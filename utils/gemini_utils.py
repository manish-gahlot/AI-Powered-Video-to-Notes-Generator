# utils/gemini_utils.py
import os
import google.generativeai as genai  # <-- Changed import
from dotenv import load_dotenv
from typing import Optional
import textwrap
# from langchain_google_genai import ChatGoogleGenerativeAI  # <-- Removed LangChain

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")  # user must set this in .env

# --- START OF MODIFIED INITIALIZATION ---
llm = None
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        
        # Set temperature and other settings
        generation_config = {
            "temperature": 0.7,
        }

        # Initialize the native Google model
        llm = genai.GenerativeModel(
            model_name="gemini-2.5-flash",  # <-- Fixed model name
            generation_config=generation_config
        )
    except Exception as e:
        print(f"Error initializing Gemini model: {e}")
        llm = None
# --- END OF MODIFIED INITIALIZATION ---


def _build_prompt(transcript: str, translate_first: bool = True) -> str:
    if translate_first:
        instruction = textwrap.dedent("""
        You are a bilingual assistant skilled at summarizing meeting or lecture transcripts. The transcript below may contain English and Hindi (Hinglish).

        Your task is to:
        1.  **Translate:** First, identify and translate any Hindi or Hinglish segments into clear, natural English. Keep the timestamps associated with the original segments.
        2.  **Summarize:** Based *only* on the fully English version (original English + translated Hindi), produce structured notes using Markdown formatting. The notes should include the following sections:

            * **## Title**
                * Create a concise, descriptive title for the transcript content (one line).

            * **## Key Takeaways**
                * Provide 2-3 main conclusions or most important points from the discussion.

            * **## Summary Points**
                * List 6-12 bullet points covering the core arguments, key information presented, decisions made, and significant questions raised.
                * Each point should be 1-2 sentences.
                * Include relevant timestamps `[start-end]` where appropriate to reference specific moments in the transcript.

            * **## Key Definitions** (Omit this section if none are found)
                * List any important terms or concepts defined in the transcript, along with their definitions.
                * Include timestamps `[start-end]` for context.

            * **## Action Items / Next Steps** (Omit this section if none are found)
                * List specific tasks, follow-ups, or next steps mentioned.
                * For each item, clearly state the task, who is responsible (if mentioned), and any deadlines mentioned.
                * Include timestamps `[start-end]`.

        Maintain a concise, objective, and professional tone throughout the notes. Ensure all information accurately reflects the content of the transcript.
        """).strip()
    else:
        # Instruction for English-only transcripts
        instruction = textwrap.dedent("""
        You are an expert assistant skilled at summarizing meeting or lecture transcripts in English.

        Your task is to produce structured notes from the transcript below using Markdown formatting. The notes should include the following sections:

            * **## Title**
                * Create a concise, descriptive title for the transcript content (one line).

            * **## Key Takeaways**
                * Provide 2-3 main conclusions or most important points from the discussion.

            * **## Summary Points**
                * List 6-12 bullet points covering the core arguments, key information presented, decisions made, and significant questions raised.
                * Each point should be 1-2 sentences.
                * Include relevant timestamps `[start-end]` where appropriate to reference specific moments in the transcript.

            * **## Key Definitions** (Omit this section if none are found)
                * List any important terms or concepts defined in the transcript, along with their definitions.
                * Include timestamps `[start-end]` for context.

            * **## Action Items / Next Steps** (Omit this section if none are found)
                * List specific tasks, follow-ups, or next steps mentioned.
                * For each item, clearly state the task, who is responsible (if mentioned), and any deadlines mentioned.
                * Include timestamps `[start-end]`.

        Maintain a concise, objective, and professional tone throughout the notes. Ensure all information accurately reflects the content of the transcript.
        """).strip()

    prompt = instruction + "\n\nTranscript:\n" + transcript
    return prompt

def summarize_transcript_with_gemini(transcript: str, translate_first: bool = True) -> str:
    """
    Summarize using Gemini Flash via native library. Fallback to simple heuristic if Gemini fails.
    """
    prompt = _build_prompt(transcript, translate_first=translate_first)

    if llm:
        try:
            # --- START OF MODIFIED API CALL ---
            # Use .generate_content() and access the .text attribute
            response = llm.generate_content(prompt)
            text = response.text
            # --- END OF MODIFIED API CALL ---
            return text
        except Exception as e:
            # Fallback
            fallback_text = _heuristic_summary(transcript)
            return f"(Fallback summary due to Gemini error: {e})\n\n{fallback_text}"
    else:
        fallback_text = _heuristic_summary(transcript)
        return f"(Gemini not available — returning fallback summary)\n\n{fallback_text}"


def _heuristic_summary(transcript: str) -> str:
    """
    Simple fallback: take first N lines, cluster into bullets.
    """
    # This function is perfect, no changes needed.
    lines = [l.strip() for l in transcript.splitlines() if l.strip()]
    bullets = []
    for ln in lines[:12]:
        bullets.append(f"- {ln[:200]}")
    title = "Notes (auto)"
    notes = f"{title}\n\n" + "\n".join(bullets)
    return notes