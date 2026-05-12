import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.sunbird.ai"
TOKEN = os.getenv("SUNBIRD_API_TOKEN", "")

LANGUAGE_CODES = {
    "English":    "eng",
    "Luganda":    "lug",
    "Runyankole": "nyn",
    "Ateso":      "teo",
    "Lugbara":    "lgg",
    "Acholi":     "ach",
}

TTS_SPEAKER_IDS = {
    "Luganda":    248,
    "Runyankole": 243,
    "Ateso":      242,
    "Lugbara":    245,
    "Acholi":     241,
    "English":    248,
}

LOCAL_LANGUAGES = ["Luganda", "Runyankole", "Ateso", "Lugbara", "Acholi"]
ALL_LANGUAGES   = ["English"] + LOCAL_LANGUAGES


def _session():
    """Create a requests session with automatic retries."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


def _auth_headers() -> dict:
    if not TOKEN:
        raise RuntimeError(
            "SUNBIRD_API_TOKEN is not set. "
            "Add it to your .env file."
        )
    return {"Authorization": f"Bearer {TOKEN}"}


def transcribe(audio_path: str) -> str:
    """POST /tasks/stt"""
    with open(audio_path, "rb") as f:
        response = _session().post(
            f"{BASE_URL}/tasks/stt",
            headers=_auth_headers(),
            files={"audio": f},
            timeout=180,
        )
    response.raise_for_status()
    return response.json()["output"]["text"]


def summarise(text: str) -> str:
    """POST /tasks/summarise"""
    response = _session().post(
        f"{BASE_URL}/tasks/summarise",
        headers={**_auth_headers(), "Content-Type": "application/json"},
        json={"text": text},
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["summarized_text"]


def sunflower_chat(system_prompt: str, user_message: str) -> str:
    """POST /tasks/sunflower_inference"""
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ]
    }
    response = _session().post(
        f"{BASE_URL}/tasks/sunflower_inference",
        headers={**_auth_headers(), "Content-Type": "application/json"},
        json=payload,
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["content"]


def translate(text: str, target_language: str) -> str:
    return sunflower_chat(
        system_prompt=(
            f"You are a professional translator specialising in Ugandan languages. "
            f"Translate the following text into {target_language}. "
            f"Return only the translated text, nothing else."
        ),
        user_message=text,
    )


def translate_direct(text: str, source_language: str, target_language: str) -> str:
    return sunflower_chat(
        system_prompt=(
            f"You are a professional translator. Translate the following text from "
            f"{source_language} to {target_language}. Return only the translated text."
        ),
        user_message=text,
    )


def synthesise(text: str, language: str) -> str:
    """POST /tasks/tts"""
    speaker_id = TTS_SPEAKER_IDS.get(language, 248)
    response = _session().post(
        f"{BASE_URL}/tasks/tts",
        headers={**_auth_headers(), "Content-Type": "application/json"},
        json={"text": text, "speaker_id": speaker_id},
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["output"]["audio_url"]


def download_audio(audio_url: str, dest_path: str) -> str:
    """Download signed audio URL to a local file."""
    r = _session().get(audio_url, timeout=60)
    r.raise_for_status()
    with open(dest_path, "wb") as f:
        f.write(r.content)
    return dest_path