"""Desktop automation command adapter."""

from __future__ import annotations

import threading
import time
from pathlib import Path

import pyautogui as gui
import pywhatkit

from Automation.Battery import check_percentage
from Automation.Play_Music_YT import play_music_on_youtube
from Automation.Web_Open import openweb
from Automation.open_App import open_App
from Automation.playmusic_Sfy import play_music_on_spotify
from Automation.scrool_system import perform_scroll_action
from Automation.tab_automation import perform_browser_action
from Automation.Youtube_play_back import perform_media_action
from TextToSpeech.Fast_DF_TTS import speak


RUNTIME_INPUT = Path(".runtime") / "input.txt"


def play() -> None:
    gui.press("space")


def search_google(text: str) -> None:
    pywhatkit.search(text)


def close() -> None:
    gui.hotkey("alt", "f4")


def search(text: str) -> None:
    gui.press("/")
    time.sleep(0.3)
    gui.write(text, interval=0.01)


def clear_file() -> None:
    RUNTIME_INPUT.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_INPUT.write_text("", encoding="utf-8")


def _wait_for_song() -> str:
    """Wait for the STT layer to write a command containing a song."""
    previous = ""
    while True:
        try:
            current = RUNTIME_INPUT.read_text(encoding="utf-8").strip().lower()
        except FileNotFoundError:
            clear_file()
            current = ""
        if current and current != previous:
            previous = current
            if current.endswith("song"):
                return current
        time.sleep(0.15)


def Open_Brain(text: str) -> None:
    """Open a known website or Windows application."""
    cleaned = text.strip()
    if "website" in cleaned or "open website named" in cleaned:
        target = cleaned.replace("open website named", "").replace("website", "").replace("open", "").strip()
        speak(f"Navigating to {target}.")
        openweb(target)
        return

    target = cleaned.replace("app", "").replace("open", "").strip()
    speak(f"Opening {target}.")
    open_App(target)


def Auto_main_brain(text: str) -> None:
    """Dispatch a desktop automation command."""
    command = text.strip().lower()
    if not command:
        return

    try:
        if command.startswith("open"):
            Open_Brain(command)
        elif "close" in command:
            close()
        elif "play music" in command or "play music on youtube" in command:
            speak("Which song would you like to play?")
            clear_file()
            play_music_on_youtube(_wait_for_song())
        elif "play some music" in command or "play music on spotify" in command:
            speak("Which song would you like to play?")
            clear_file()
            play_music_on_spotify(_wait_for_song())
        elif "check battery percentage" in command or "check battery level" in command:
            check_percentage()
        elif command.startswith("search in google"):
            query = command.replace("search in google", "", 1).strip()
            speak(f"Searching Google for {query}.")
            threading.Thread(target=search_google, args=(query,), daemon=True).start()
        elif command.startswith("search"):
            query = command.replace("search", "", 1).strip()
            speak(f"Searching for {query}.")
            search(query)
            gui.press("enter")
        elif any(term in command for term in ("play", "stop", "pause")):
            play()
        else:
            perform_browser_action(command)
            perform_media_action(command)
            perform_scroll_action(command)
    except Exception as exc:
        print(f"Automation error: {exc}")
