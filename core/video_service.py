import os
import subprocess
from models.schemas import VideoMetadata
from config.settings import TEMP_DIR

def get_local_video_metadata(file_path: str) -> VideoMetadata:
    file_name = os.path.basename(file_path)
    # Basic fallback metadata for uploaded files
    return VideoMetadata(
        video_id=f"local_{hash(file_path)}",
        title=os.path.splitext(file_name)[0].replace("_", " ").title(),
        duration_seconds=0.0,
        duration_formatted="Uploaded File",
        source_type='upload',
        url_or_path=file_path,
        uploader="Local User",
        upload_date="Today",
        view_count="1",
        thumbnail_url=None
    )

def extract_audio_from_local_video(video_path: str) -> str:
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(TEMP_DIR, f"{base_name}_audio.mp3")
    
    cmd = [
        'ffmpeg', '-y', '-i', video_path,
        '-vn', '-acodec', 'libmp3lame', '-q:a', '2', audio_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return audio_path