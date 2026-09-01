"""Command orchestration for the Gandalf desktop agent."""

from __future__ import annotations

import threading
import time
from pathlib import Path

from Automation.Automation_Brain import Auto_main_brain
from Brain.brain import Main_Brain
from Features.br_persentage import check_br_persentage
from Features.check_running_app import check_running_app
from Features.create_file import create_file
from Features.mike_health import mike_health
from Features.set_br import set_brightness_windows
from Features.set_get_volume import get_volume_windows, set_volume_windows
from Features.speaker_health import speaker_health_test
from NetHyTechSTT.listen import listen
from TextToImage.gen_image import generate_image
from TextToSpeech.Fast_DF_TTS import speak
from Time_Operations.brain import input_manage, input_manage_Alam
from Vision.MVbrain import capture_image_and_save as capture_mobile_image
from Vision.MVbrain import encode_image_to_base64 as encode_mobile_image
from Vision.MVbrain import mobile_vision_brain
from Vision.Vbrain import capture_image_and_save
from Vision.Vbrain import encode_image_to_base64, vision_brain
from Weather_Check.check_weather import get_weather_by_address
from Whatsapp_automation.wa import send_msg_wa
from core.command_utils import normalize_spoken_time, parse_percentage


RUNTIME_DIR = Path(".runtime")
INPUT_FILE = RUNTIME_DIR / "input.txt"
CAPTURED_IMAGE = RUNTIME_DIR / "captured_image.png"


def _read_input() -> str:
    """Read the latest STT command without failing on missing runtime state."""
    try:
        return INPUT_FILE.read_text(encoding="utf-8").strip().lower()
    except FileNotFoundError:
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        INPUT_FILE.touch()
        return ""


def _clear_input() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    INPUT_FILE.write_text("", encoding="utf-8")


def _handle_vision() -> None:
    if capture_image_and_save(str(CAPTURED_IMAGE)):
        answer = vision_brain(encode_image_to_base64(str(CAPTURED_IMAGE)))
        speak(answer)


def _handle_mobile_vision() -> None:
    if capture_mobile_image(str(CAPTURED_IMAGE)):
        answer = mobile_vision_brain(encode_mobile_image(str(CAPTURED_IMAGE)))
        speak(answer)


def _handle_command(command: str) -> None:
    """Dispatch one normalized command to the appropriate capability."""
    if command.startswith("tell me"):
        input_manage(normalize_spoken_time(command))
        _clear_input()
        return

    if command.startswith("set alarm"):
        input_manage_Alam(normalize_spoken_time(command))
        _clear_input()
        return

    if "jarvis" in command:
        speak(Main_Brain(command))
        return

    if command.startswith("create") and "file" in command:
        create_file(command)
        return

    # Keep the more specific mobile-camera command ahead of the generic vision command.
    if (
        "what is in front of mobile camera" in command
        or "what can you see use mobile camera" in command
    ):
        _handle_mobile_vision()
        return

    if "what is this" in command or "what can you see" in command:
        _handle_vision()
        return

    if "check weather" in command:
        location = command.replace("check weather in", "", 1).strip()
        speak(get_weather_by_address(location))
        return

    if "send message on whatsapp" in command:
        send_msg_wa()
        return

    if command.startswith("generate image"):
        prompt = command.replace("generate image", "", 1).strip()
        if prompt:
            speak(
                "Image generation completed."
                if generate_image(prompt)
                else "Image generation failed."
            )
        return

    if any(term in command for term in ("check mike", "check microphone")):
        mike_health()
        return

    if "check speaker" in command:
        speaker_health_test()
        return

    if "check brightness percentage" in command:
        check_br_persentage()
        return

    if "set brightness percentage" in command:
        value = command.replace("set brightness percentage", "", 1).strip()
        set_brightness_windows(parse_percentage(value))
        return

    if "check volume level" in command:
        get_volume_windows()
        return

    if "set volume level" in command:
        value = command.replace("set volume level", "", 1).strip()
        set_volume_windows(parse_percentage(value))
        return

    if "check running application" in command:
        check_running_app()
        return

    Auto_main_brain(command)


def check_inputs(poll_interval: float = 0.15) -> None:
    """Poll the STT handoff file and dispatch new commands."""
    last_input = ""
    while True:
        command = _read_input()
        if command and command != last_input:
            last_input = command
            try:
                _handle_command(command)
            except (ValueError, TypeError) as exc:
                print(f"Command validation error: {exc}")
            except Exception as exc:
                print(f"Command execution error: {exc}")
        time.sleep(poll_interval)


def Jarvis() -> None:
    """Start speech recognition and command orchestration."""
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    _clear_input()
    listener = threading.Thread(target=listen, daemon=True)
    command_loop = threading.Thread(target=check_inputs, daemon=True)
    listener.start()
    command_loop.start()
    listener.join()
    command_loop.join()
