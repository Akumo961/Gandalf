"""Text-to-speech adapter with bounded network calls and safe cleanup."""

from __future__ import annotations

import os
import sys
import tempfile
import threading
import time
from pathlib import Path
from urllib.parse import urlencode

import requests
from playsound import playsound


TTS_ENDPOINT = os.getenv(
    "GANDALF_TTS_ENDPOINT",
    "https://api.streamelements.com/kappa/v2/speech",
)
DEFAULT_VOICE = os.getenv("GANDALF_TTS_VOICE", "Matthew")
REQUEST_TIMEOUT = float(os.getenv("GANDALF_REQUEST_TIMEOUT", "30"))


def generate_audio(message: str, voice: str = DEFAULT_VOICE) -> bytes | None:
    """Request synthesized audio from the configured TTS provider."""
    if not message.strip():
        return None

    params = urlencode({"voice": voice, "text": message})
    try:
        response = requests.get(
            f"{TTS_ENDPOINT}?{params}",
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": "Gandalf-AI-Agent/1.0"},
        )
        response.raise_for_status()
        return response.content
    except requests.RequestException as exc:
        print(f"TTS provider error: {exc}")
        return None


def print_animated_message(message: str) -> None:
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.025)
    print()


def Co_speak(
    message: str,
    voice: str = DEFAULT_VOICE,
    folder: str = "",
    extension: str = ".mp3",
) -> None:
    """Play generated speech and remove its temporary audio file."""
    audio = generate_audio(message, voice)
    if not audio:
        return

    temp_dir = Path(folder) if folder else Path(tempfile.gettempdir())
    temp_dir.mkdir(parents=True, exist_ok=True)
    file_path = temp_dir / f"gandalf_tts_{threading.get_ident()}{extension}"

    try:
        file_path.write_bytes(audio)
        playsound(str(file_path))
    except Exception as exc:
        print(f"Audio playback error: {exc}")
    finally:
        file_path.unlink(missing_ok=True)


def speak(text: str) -> None:
    """Speak text while displaying it to the console."""
    if not text:
        return
    speech_thread = threading.Thread(target=Co_speak, args=(text,), daemon=True)
    output_thread = threading.Thread(
        target=print_animated_message, args=(text,), daemon=True
    )
    speech_thread.start()
    output_thread.start()
    speech_thread.join()
    output_thread.join()
