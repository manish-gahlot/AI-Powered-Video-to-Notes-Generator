# app.py
import os
import uuid
import shutil
import time
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from utils.youtube_utils import download_youtube_audio, save_uploaded_video_and_extract_audio
from utils.stt_utils import transcribe_audio
from utils.gemini_utils import summarize_transcript_with_gemini
from utils.pdf_utils import create_pdf_from_notes
from utils.cleanup_utils import purge_old_temp_files, safe_remove

load_dotenv()

# Config
TEMP_DIR = Path(os.getenv("TEMP_DIR", "data/temp"))
TEMP_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_WHISPER_MODEL = os.getenv("WHISPER_MODEL", "medium")
DEFAULT_DEVICE = os.getenv("DEVICE", "cpu")
CLEANUP_HOURS = int(os.getenv("CLEANUP_OLDER_THAN_HOURS", "24"))

st.set_page_config(page_title="Video → Notes (Streamlit)", layout="centered")

st.title("🎥 ➜ 📝 Video → Notes (YouTube / Upload)")
st.markdown("Upload a video file or paste a YouTube URL. The app will transcribe (faster-whisper), translate/summarize (Gemini Flash) and export a PDF (ReportLab).")

# Cleanup on app start (remove older temp files)
with st.spinner("Cleaning up old temp files..."):
    purge_old_temp_files(TEMP_DIR, older_than_hours=CLEANUP_HOURS)

col1, col2 = st.columns(2)
with col1:
    youtube_url = st.text_input("YouTube URL (paste here)", value="")
with col2:
    uploaded_file = st.file_uploader("Or upload a local video", type=["mp4", "mkv", "webm", "mov", "avi"])

st.markdown("---")
st.write("**Processing options**")
model = st.selectbox("Whisper model (faster-whisper)", options=["small", "medium", "large-v2"], index=1)
device = st.selectbox("Device", options=["cpu", "cuda"], index=0)
translate_first = st.checkbox("Translate Hindi → English before summarizing (recommended for Hinglish)", value=True)
keep_temp = st.checkbox("Keep temporary files after processing", value=False)

process_button = st.button("Process video → generate PDF")

if process_button:
    run_id = f"{int(time.time())}_{uuid.uuid4().hex[:8]}"
    run_dir = TEMP_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    try:
        # 1) Get audio path
        if youtube_url.strip():
            st.info("Downloading audio from YouTube...")
            audio_path = run_dir / "audio.wav"
            with st.spinner("Downloading audio (yt-dlp + ffmpeg)..."):
                download_youtube_audio(youtube_url.strip(), str(audio_path))
            st.success(f"Downloaded audio: {audio_path.name}")
        elif uploaded_file is not None:
            st.info("Saving uploaded video & extracting audio...")
            uploaded_video_path = run_dir / uploaded_file.name
            with open(uploaded_video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            audio_path = run_dir / "audio.wav"
            with st.spinner("Extracting audio with ffmpeg..."):
                save_uploaded_video_and_extract_audio(str(uploaded_video_path), str(audio_path))
            st.success("Audio extracted.")
        else:
            st.error("Please provide either a YouTube URL or upload a video file.")
            safe_remove(run_dir)
            st.stop()

        # 2) Transcribe
        st.info("Transcribing audio with faster-whisper...")
        with st.spinner("Transcribing (this may take a while)..."):
            segments, transcript_text = transcribe_audio(
                audio_file=str(audio_path),
                model_name=model,
                device=device,
                run_dir=str(run_dir)
            )
        st.success("Transcription complete.")
        st.text_area("Transcript (first 4000 chars)", value=transcript_text[:4000], height=200)

        # 3) Summarize with Gemini (translate-first option)
        st.info("Summarizing with Gemini Flash (or fallback)...")
        with st.spinner("Calling Gemini..."):
            final_notes = summarize_transcript_with_gemini(transcript_text, translate_first=translate_first)
        st.success("Summarization complete.")
        st.markdown("**Summary Preview:**")
        st.text_area("Notes preview", value=final_notes[:4000], height=300)

        # 4) Generate PDF
        st.info("Generating PDF...")
        pdf_path = run_dir / f"notes_{run_id}.pdf"
        create_pdf_from_notes(title="Video Notes", notes_text=final_notes, output_path=str(pdf_path))
        st.success("PDF generated.")
        with open(pdf_path, "rb") as f:
            st.download_button("Download notes PDF", data=f, file_name=pdf_path.name, mime="application/pdf")

        # 5) Cleanup if requested
        if not keep_temp:
            st.info("Cleaning up temporary files...")
            safe_remove(run_dir)
            st.success("Temporary files removed.")
        else:
            st.info(f"Temporary files kept at: {run_dir}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.exception(e)
        # try to cleanup partial results
        if run_dir.exists():
            safe_remove(run_dir)
