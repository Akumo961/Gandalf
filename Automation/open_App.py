"""Safe Windows application launcher."""

from __future__ import annotations

import shlex
import subprocess
import time

import pyautogui as gui


def open_App(text: str) -> bool:
    """Try to launch a simple Windows application name.

    The command is parsed without a shell, avoiding shell injection through
    model-generated text. The Start-menu fallback is retained for GUI apps.
    """
    target = text.strip()
    if not target:
        return False

    try:
        args = shlex.split(target, posix=False)
        if not args:
            return False
        subprocess.Popen(args, shell=False)
        return True
    except (OSError, ValueError):
        try:
            gui.press("win")
            time.sleep(0.2)
            gui.write(target, interval=0.01)
            time.sleep(0.2)
            gui.press("enter")
            return True
        except Exception as exc:
            print(f"Application launch error: {exc}")
            return False
