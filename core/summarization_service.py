import json
import re
from openai import OpenAI
from config.settings import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from prompts.summarization_prompts import SYSTEM_PROMPT, build_user_prompt
from models.schemas import SummaryResult

def get_llm_client() -> OpenAI:
    return OpenAI(api_key=LLM_API_KEY or "dummy", base_url=LLM_BASE_URL)

def generate_ai_summary(transcript_text: str, length: str = "Medium", language: str = "English") -> SummaryResult:
    client = get_llm_client()
    user_prompt = build_user_prompt(transcript_text, length, language)
    
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    
    raw_content = response.choices[0].message.content.strip()
    
    # Strip markdown wrapper if present
    cleaned = re.sub(r"^```json\s*", "", raw_content)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    
    try:
        data = json.loads(cleaned)
        return SummaryResult(**data)
    except Exception as e:
        # Fallback structured response in case of parsing issue
        return SummaryResult(
            title="Video Summary",
            summary_paragraph="Failed to parse LLM structured output. Raw response captured.",
            key_points=[raw_content[:200]],
            highlights=[],
            chapters=[]
        )