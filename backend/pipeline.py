import os
import tempfile
from mutagen import File as MutagenFile
from backend.sunbird_client import (
    transcribe,
    summarise,
    translate,
    synthesise,
    download_audio,
)

MAX_AUDIO_SECONDS = 300  # 5 minutes


def get_audio_duration_seconds(path: str) -> float:
    audio = MutagenFile(path)
    if audio is None:
        raise ValueError("Could not read audio file. Ensure it is MP3, WAV, OGG, M4A, or AAC.")
    return audio.info.length


def run_pipeline(
    text_input,
    audio_path,
    target_language,
):
    if not audio_path and not (text_input and text_input.strip()):
        raise ValueError("Provide either text input or an audio file.")

    transcript = None

    if audio_path:
        duration = get_audio_duration_seconds(audio_path)
        if duration > MAX_AUDIO_SECONDS:
            raise ValueError(
                f"Audio is {duration:.0f} s long — exceeds the 5-minute limit. "
                "Please upload a shorter clip."
            )
        transcript = transcribe(audio_path)
        working_text = transcript
    else:
        working_text = text_input.strip()

    summary = summarise(working_text)
    translated = translate(summary, target_language)
    audio_url = synthesise(translated, target_language)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=tempfile.gettempdir())
    tmp.close()
    local_audio = download_audio(audio_url, tmp.name)

    return transcript, summary, translated, local_audio