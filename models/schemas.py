from pydantic import BaseModel, Field
from typing import List, Optional

class Highlight(BaseModel):
    timestamp: str = Field(description="Format MM:SS or HH:MM:SS")
    title: str
    duration: str = Field(description="Format MM:SS")
    description: str

class Chapter(BaseModel):
    timestamp: str = Field(description="Format MM:SS or HH:MM:SS")
    title: str
    description: str

class SummaryResult(BaseModel):
    title: str
    summary_paragraph: str
    key_points: List[str]
    highlights: List[Highlight]
    chapters: List[Chapter]

class VideoMetadata(BaseModel):
    video_id: str
    title: str
    duration_seconds: float
    duration_formatted: str
    source_type: str  
    url_or_path: str
    uploader: Optional[str] = "Unknown"
    upload_date: Optional[str] = "N/A"
    view_count: Optional[str] = "N/A"
    thumbnail_url: Optional[str] = None