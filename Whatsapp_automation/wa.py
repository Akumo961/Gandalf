"""Optional WhatsApp automation adapter.

This integration is configuration-driven: no phone numbers or message history
are stored in source control.
"""

from __future__ import annotations

import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import pywhatkit as kit

from TextToSpeech.Fast_DF_TTS import speak


RUNTIME_INPUT = Path(".runtime") / "input.txt"
RECIPIENT = os.getenv("GANDALF_WHATSAPP_RECIPIENT", "")


def _read_input() -> str:
    try:
        return RUNTIME_INPUT.read_text(encoding="utf-8").strip().lower()
    except FileNotFoundError:
        return ""


def _clear_input() -> None:
    RUNTIME_INPUT.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_INPUT.write_text("", encoding="utf-8")


def send_msg_wa() -> bool:
    """Send a WhatsApp message to the configured recipient after confirmation."""
    if not RECIPIENT:
        speak("WhatsApp is not configured. Set GANDALF_WHATSAPP_RECIPIENT first.")
        return False

    speak("Who do you want to send the message to?")
    previous = ""
    while True:
        current = _read_input()
        if current and current != previous:
            previous = current
            if current.startswith(("send to", "send tu")):
                speak("What is the message?")
                _clear_input()
                break
        time.sleep(0.15)

    previous = ""
    while True:
        current = _read_input()
        if current and current != previous:
            previous = current
            if current.startswith("message is"):
                message = current.replace("message is", "", 1).strip()
                if not message:
                    speak("The message is empty.")
                    return False
                try:
                    scheduled = datetime.now() + timedelta(minutes=1)
                    kit.sendwhatmsg(
                        RECIPIENT,
                        message,
                        scheduled.hour,
                        scheduled.minute,
                    )
                    speak("Message scheduled successfully.")
                    return True
                except Exception as exc:
                    print(f"WhatsApp automation error: {exc}")
                    speak("I couldn't schedule the WhatsApp message.")
                    return False
        time.sleep(0.15)
