import json
import re
import time
from typing import List
from openai import OpenAI
from config.settings import (
    LLM_API_KEY, LLM_BASE_URL, LLM_MODEL,
    TOKEN_CHUNK_SIZE, TOKEN_OVERLAP, 
    MAX_REDUCE_TOKENS, TPM_DELAY_SECONDS
)
from prompts.summarization_prompts import (
    SYSTEM_PROMPT, 
    CHUNK_SUMMARY_PROMPT, 
    build_reduce_prompt, 
    build_user_prompt
)
from models.schemas import SummaryResult

def get_llm_client() -> OpenAI:
    return OpenAI(api_key=LLM_API_KEY or "dummy", base_url=LLM_BASE_URL)

def estimate_tokens(text: str) -> int:
    """Robust token estimation: roughly 1 token per 4 characters / 0.75 words."""
    words = len(text.split())
    chars = len(text)
    return int(max(words * 1.33, chars / 4.0)) + 50

def chunk_transcript_by_tokens(text: str, max_tokens: int = TOKEN_CHUNK_SIZE, overlap_tokens: int = TOKEN_OVERLAP) -> List[str]:
    """Splits transcript into overlapping chunks based on strict token estimations."""
    if estimate_tokens(text) <= max_tokens:
        return [text]
        
    words = text.split()
    chunks = []
    start_idx = 0
    total_words = len(words)
    
    words_per_chunk = int(max_tokens / 1.33)
    overlap_words = int(overlap_tokens / 1.33)
    
    while start_idx < total_words:
        end_idx = min(start_idx + words_per_chunk, total_words)
        chunk_text = " ".join(words[start_idx:end_idx])
        chunks.append(chunk_text)
        
        if end_idx == total_words:
            break
            
        start_idx = end_idx - overlap_words
        
    return chunks

def generate_ai_summary(transcript_text: str, length: str = "Medium") -> SummaryResult:
    client = get_llm_client()
    total_tokens = estimate_tokens(transcript_text)
    
    if total_tokens <= TOKEN_CHUNK_SIZE:  # for short transcripts like under 10 mins
        user_prompt = build_user_prompt(transcript_text, length)
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        return parse_json_response(response.choices[0].message.content.strip())

    # for long transcripts
    chunks = chunk_transcript_by_tokens(transcript_text, TOKEN_CHUNK_SIZE, TOKEN_OVERLAP)
    intermediate_summaries = []
    
    # 1. Map Phase: Summarize each chunk independently
    for idx, chunk in enumerate(chunks):
        chunk_prompt = CHUNK_SUMMARY_PROMPT.format(chunk_text=chunk)
        
        if idx > 0:
            time.sleep(TPM_DELAY_SECONDS)
            
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a highly precise, extremely concise transcript analyzer. English only."},
                {"role": "user", "content": chunk_prompt}
            ],
            temperature=0.1 # Low temp for strict fact extraction
        )
        summary = response.choices[0].message.content.strip()
        intermediate_summaries.append(f"--- Section {idx + 1} Summary ---\n{summary}")

    # 2. Reduce Phase Preparation
    combined_text = "\n\n".join(intermediate_summaries)
    
    # Recursive Reduce: If intermediate summaries are STILL too large, compact them further
    while estimate_tokens(combined_text) > MAX_REDUCE_TOKENS:
        time.sleep(TPM_DELAY_SECONDS)
        compaction_prompt = f"Condense the following summaries. Retain all key facts and timestamps, but make it shorter:\n\n{combined_text[:15000]}"
        compact_res = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": compaction_prompt}],
            temperature=0.2
        )
        combined_text = compact_res.choices[0].message.content.strip()

    # 3. Final Reduce Synthesis
    time.sleep(TPM_DELAY_SECONDS)
    reduce_prompt = build_reduce_prompt(combined_text, length)
    
    final_response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": reduce_prompt}
        ],
        temperature=0.3
    )
    
    return parse_json_response(final_response.choices[0].message.content.strip())

def parse_json_response(raw_content: str) -> SummaryResult:
    """Cleans Markdown formatting and parses response into SummaryResult schema."""
    cleaned = re.sub(r"^```json\s*", "", raw_content, flags=re.MULTILINE)
    cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
    cleaned = cleaned.strip()
    
    try:
        data = json.loads(cleaned)
        return SummaryResult(**data)
    except Exception as e:
        return SummaryResult(
            title="Video Summary",
            summary_paragraph=f"Failed to parse structured summary. Raw response: {cleaned[:500]}...",
            key_points=[f"Parsing error occurred: {str(e)}"],
            highlights=[],
            chapters=[]
        )