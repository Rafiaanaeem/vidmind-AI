import os
import re
from typing import Dict, Any, Optional, List

import yt_dlp
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)

from models.schemas import VideoMetadata
from config.settings import TEMP_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(TEMP_DIR, exist_ok=True)
COOKIES_FILE = None

for name in ["youtube_cookies.txt", "cookies.txt"]:
    candidate = os.path.join(BASE_DIR, name)

    if os.path.exists(candidate):
        COOKIES_FILE = candidate
        print(f"[YouTube] Using cookies: {candidate}")
        break

def extract_youtube_id(url: str) -> Optional[str]:
    """
    Extract an 11-character YouTube video ID from common
    YouTube URL formats.
    """

    patterns = [
        r"(?:v=)([a-zA-Z0-9_-]{11})",
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})",
        r"(?:youtube\.com/live/)([a-zA-Z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None

def get_base_ydl_options() -> Dict[str, Any]:
    """
    Common yt-dlp configuration.
    """
    options = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "ignoreerrors": False,

        "extractor_args": {
            "youtube": {
                "player_client": ["default"],
            }
        },
    }

    if COOKIES_FILE:
        options["cookiefile"] = COOKIES_FILE

    return options

# for meta data
def get_youtube_metadata(url: str) -> VideoMetadata:
    """
    Extract YouTube video metadata without downloading the video.
    """
    ydl_opts = get_base_ydl_options()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=False)
        if not info:
            raise RuntimeError(
                "Unable to retrieve YouTube video information."
            )

        video_id = info.get("id", "")

        duration_sec = int(info.get("duration", 0) or 0)

        mins = duration_sec // 60
        secs = duration_sec % 60

        duration_str = f"{mins}:{secs:02d}"

        raw_views = info.get("view_count", 0) or 0
        formatted_views = f"{raw_views:,}"

        return VideoMetadata(
            video_id=video_id,
            title=info.get("title", "YouTube Video"),
            source_type="youtube",
            url_or_path=url,
            duration_seconds=duration_sec,
            duration_formatted=duration_str,
            uploader=info.get("uploader", "Unknown Uploader"),
            view_count=formatted_views,
        )

# for transcript generation
def get_youtube_transcript(
    video_id: str,
) -> Optional[List[Dict[str, Any]]]:
    """
    Try to retrieve an existing YouTube transcript.

    Compatible with newer youtube-transcript-api versions.
    """
    try:

        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcript = None

        try:
            transcript = transcript_list.find_manually_created_transcript(
                ["en"]
            )
        except Exception:
            pass

        # use english transcript
        if transcript is None:

            try:
                transcript = transcript_list.find_generated_transcript(
                    ["en"]
                )
            except Exception:
                pass

        # If English isn't available, use the first transcript
        if transcript is None:

            try:
                transcript = next(iter(transcript_list))
            except StopIteration:
                return None

        fetched = transcript.fetch()

        results = []

        for item in fetched:

            if hasattr(item, "text"):

                results.append({
                    "start": float(item.start),
                    "duration": float(item.duration),
                    "text": item.text,
                })

            else:

                results.append({
                    "start": float(item["start"]),
                    "duration": float(item["duration"]),
                    "text": item["text"],
                })

        if not results:
            return None

        print(
            f"[YouTube] Transcript found: "
            f"{len(results)} segments"
        )

        return results

    except (
        TranscriptsDisabled,
        NoTranscriptFound,
    ):

        print("[YouTube] No transcript available.")

        return None

    except Exception as e:

        print(
            f"[YouTube] Transcript retrieval failed: {e}"
        )

        return None


# for audio download
def download_youtube_audio(url: str) -> str:
    """
    Download the best available audio from YouTube
    and convert it to MP3 using FFmpeg.
    """
    video_id = extract_youtube_id(url) or "yt_audio"
    final_path = os.path.join(
        TEMP_DIR,
        f"{video_id}.mp3"
    )

    # Use cached audio if already downloaded
    if os.path.exists(final_path):
        print(f"[YouTube] Using cached audio: {final_path}")
        return final_path

    output_template = os.path.join(
        TEMP_DIR,
        f"{video_id}.%(ext)s"
    )

    ydl_opts = {
        # yt-dlp will choose the best available audio.
        "format": "bestaudio/best",

        "outtmpl": output_template,

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],

        "quiet": False,
        "no_warnings": False,
        "noplaylist": True,
    }

    if COOKIES_FILE:
        ydl_opts["cookiefile"] = COOKIES_FILE

    print("[YouTube] Downloading audio...")

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except yt_dlp.utils.DownloadError as e:

        raise RuntimeError(
            f"Failed to download YouTube audio: {e}"
        ) from e

    if not os.path.exists(final_path):

        raise RuntimeError(
            f"Audio download completed, but expected file "
            f"was not found: {final_path}"
        )

    print(f"[YouTube] Audio ready: {final_path}")
    return final_path