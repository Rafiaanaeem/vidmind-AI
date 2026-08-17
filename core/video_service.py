import os
import ffmpeg
from models.schemas import VideoMetadata
from config.settings import TEMP_DIR

def get_local_video_metadata(file_path: str) -> VideoMetadata:
    try:
        probe = ffmpeg.probe(file_path)
        duration_sec = int(float(probe['format']['duration']))
    except Exception:
        duration_sec = 0
        
    mins = duration_sec // 60
    secs = duration_sec % 60
    duration_str = f"{mins}:{secs:02d}"
    filename = os.path.basename(file_path)

    return VideoMetadata(
        video_id=filename,
        title=filename,
        source_type='upload',
        url_or_path=file_path,
        duration_seconds=duration_sec,
        duration_formatted=duration_str,
        uploader="Local File",
        view_count="N/A"
    )

def extract_audio_from_local_video(file_path: str) -> str:
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_audio_path = os.path.join(TEMP_DIR, f"{base_name}.mp3")

    if os.path.exists(output_audio_path):
        return output_audio_path

    (
        ffmpeg
        .input(file_path)
        .output(output_audio_path, acodec='libmp3lame', ac=1, ar='16000')
        .overwrite_output()
        .run(quiet=True)
    )

    return output_audio_path