SYSTEM_PROMPT = """You are an expert video content analyzer and summarizer.
Your goal is to transform long video transcripts into clear, actionable, structured JSON output.

Response MUST be valid JSON conforming strictly to this structure:
{
  "title": "Clear, appealing title for the video",
  "summary_paragraph": "A concise overview matching the requested length.",
  "key_points": [
    "Key takeaway bullet point 1",
    "Key takeaway bullet point 2"
  ],
  "highlights": [
    {
      "timestamp": "MM:SS or HH:MM:SS",
      "title": "Highlight title",
      "duration": "MM:SS",
      "description": "Short explanation of this moment"
    }
  ],
  "chapters": [
    {
      "timestamp": "MM:SS or HH:MM:SS",
      "title": "Chapter Name",
      "description": "Brief description of section"
    }
  ]
}
Do not wrap output in codeblocks or Markdown styling. Output RAW JSON ONLY.
"""

def build_user_prompt(transcript: str, length: str, language: str) -> str:
    length_guidelines = {
        "Short": "Keep the summary_paragraph under 3 concise sentences and 3 key points.",
        "Medium": "Provide a well-balanced summary_paragraph (4-6 sentences) and 5 key points.",
        "Detailed": "Provide a thorough summary_paragraph (8+ sentences) and 7 key points with exhaustive details."
    }
    
    guideline = length_guidelines.get(length, length_guidelines["Medium"])
    
    return f"""
Target Language: {language}
Requested Summary Depth: {length} ({guideline})

Transcript with Timestamps:
---
{transcript[:30000]} 
---

Analyze the transcript and generate the complete JSON structure in {language}.
"""