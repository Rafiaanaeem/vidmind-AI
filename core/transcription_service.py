import whisper
from typing import List, Dict
from config.settings import WHISPER_MODEL

_model_cache = {}

def get_whisper_model(model_name: str = WHISPER_MODEL):
    if model_name not in _model_cache:
        _model_cache[model_name] = whisper.load_model(model_name)
    return _model_cache[model_name]

def transcribe_audio_whisper(audio_path: str) -> list:
    model = whisper.load_model("base")   # used the whisper base model
    
    result = model.transcribe(audio_path, fp16=False)
    
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": seg["start"],
            "duration": seg["end"] - seg["start"],
            "text": seg["text"].strip()
        })
    return segments

def format_transcript_with_timestamps(segments: List[Dict]) -> str:
    lines = []
    for s in segments:
        start_sec = int(s['start'])
        mins, secs = divmod(start_sec, 60)
        hrs, mins = divmod(mins, 60)
        ts = f"[{hrs:02d}:{mins:02d}:{secs:02d}]" if hrs > 0 else f"[{mins:02d}:{secs:02d}]"
        lines.append(f"{ts} {s['text']}")
    return "\n".join(lines)