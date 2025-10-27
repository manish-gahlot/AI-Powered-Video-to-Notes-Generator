# utils/youtube_utils.py
import os
import subprocess
from pathlib import Path
import yt_dlp

def download_youtube_audio(youtube_url: str, output_path: str):
    """
    Download best audio and convert to WAV (via ffmpeg).
    output_path should end with .wav
    """
    output_path = Path(output_path)
    tmp_output = output_path.with_suffix(".%(ext)s")


    ffmpeg_path = r"C:\ffmpeg\bin"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(tmp_output),
        "quiet": True,
        "no_warnings": True,
        "ffmpeg_location": ffmpeg_path, 
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    # yt-dlp + ffmpeg will produce a .wav next to template. If not, fallback:
    if not output_path.exists():
        # try to find any wav in current dir (best-effort)
        candidates = list(Path(".").glob("*.wav"))
        if candidates:
            candidates[0].rename(output_path)
    return str(output_path)

def save_uploaded_video_and_extract_audio(video_path: str, audio_output_path: str):
    """
    Use ffmpeg to extract audio to WAV
    """
    from ffmpeg import input as ff_input, output as ff_output, run as ff_run
    # Use ffmpeg-python for conversion
    stream = ff_input(video_path)
    stream = ff_output(stream.audio, audio_output_path, ar=16000, ac=1, format="wav")
    ff_run(stream, quiet=True)
    return audio_output_path
