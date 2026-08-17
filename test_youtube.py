from core.youtube_service import download_youtube_audio

url = "https://www.youtube.com/watch?v=uQ2rJKiiRiU"

try:
    audio_path = download_youtube_audio(url)

    print("\nSUCCESS!")
    print("Audio:", audio_path)

except Exception as e:
    print("\nFAILED!")
    print(e)