# utils/stt_utils.py
import os
from faster_whisper import WhisperModel
from typing import Tuple, List, Dict

def transcribe_audio(audio_file: str, model_name: str = "small", device: str = "cpu", run_dir: str = None):
    """
    Returns (segments, combined_text)
    segments is a list of dicts: { 'start': float, 'end': float, 'text': str }
    combined_text is the full transcript string
    """
    # instantiate model
    model = WhisperModel(
        model_name,
        device="cpu",
        compute_type="int8"
    )
    segments, info = model.transcribe(audio_file, language=None, beam_size=5)
    combined = []
    segment_list = []
    for segment in segments:
        # segment has start, end, text fields
        segment_txt = segment.text.strip()
        segment_list.append({
            "start": float(segment.start),
            "end": float(segment.end),
            "text": segment_txt
        })
        combined.append(segment_txt)
    full_text = "\n".join([f"[{s['start']:.2f}-{s['end']:.2f}] {s['text']}" for s in segment_list])
    return segment_list, full_text
