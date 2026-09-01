"""Gandalf application entry point."""

from __future__ import annotations

import random
import threading
from pathlib import Path

from Alert import Alert
from Automation.Battery import check_plug
from Data.DLG_Data import offline_dlg, online_dlg
from TextToSpeech.Fast_DF_TTS import speak
from Time_Operations.throw_alert import check_Alam, check_schedule
from co_brain import Jarvis
from internet_check import is_Online


RUNTIME_DIR = Path(".runtime")
SCHEDULE_FILE = RUNTIME_DIR / "schedule.txt"
ALARM_FILE = RUNTIME_DIR / "alarm_data.txt"


def main() -> None:
    """Start Gandalf's background services when network connectivity is available."""
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    online_dialogue = random.choice(online_dlg)
    offline_dialogue = random.choice(offline_dlg)

    if not is_Online():
        Alert(offline_dialogue)
        return

    startup = threading.Thread(target=speak, args=(online_dialogue,), daemon=True)
    battery = threading.Thread(target=check_plug, daemon=True)
    scheduler = threading.Thread(
        target=check_schedule, args=(str(SCHEDULE_FILE),), daemon=True
    )
    agent = threading.Thread(target=Jarvis, daemon=True)
    alarms = threading.Thread(
        target=check_Alam, args=(str(ALARM_FILE),), daemon=True
    )

    startup.start()
    startup.join()

    for worker in (battery, scheduler, agent, alarms):
        worker.start()

    for worker in (battery, scheduler, agent, alarms):
        worker.join()


if __name__ == "__main__":
    main()
