import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Tuple, List, Dict, Optional
import os
import re
from config.settings import TEMP_DIR
from models.schemas import VideoMetadata

def extract_youtube_id(url: str) -> Optional[str]:
    pattern = r'(?:v=|\/|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_youtube_metadata(url: str) -> VideoMetadata:
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_id = info.get('id', 'unknown')
        duration = info.get('duration', 0)
        
        mins, secs = divmod(int(duration), 60)
        hrs, mins = divmod(mins, 60)
        duration_fmt = f"{hrs:02d}:{mins:02d}:{secs:02d}" if hrs > 0 else f"{mins:02d}:{secs:02d}"
        
        return VideoMetadata(
            video_id=video_id,
            title=info.get('title', 'YouTube Video'),
            duration_seconds=float(duration),
            duration_formatted=duration_fmt,
            source_type='youtube',
            url_or_path=url,
            uploader=info.get('uploader', 'YouTube Channel'),
            upload_date=info.get('upload_date', 'N/A'),
            view_count=f"{info.get('view_count', 0):,}",
            thumbnail_url=info.get('thumbnail')
        )

def get_youtube_transcript(video_id: str) -> Optional[List[Dict]]:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatted = []
        for item in transcript:
            formatted.append({
                'start': item['start'],
                'duration': item['duration'],
                'text': item['text']
            })
        return formatted
    except Exception:
        return None

def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(TEMP_DIR, "%(id)s.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        return f"{base}.mp3"