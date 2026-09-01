"""LLM reasoning adapter used by Gandalf.

The provider remains isolated behind Main_Brain so the rest of the application
can evolve without coupling orchestration code to a specific LLM SDK.
"""

from __future__ import annotations

import os
from pathlib import Path

from webscout import PhindSearch


DEFAULT_HISTORY_FILE = Path(".runtime") / "chat_history.txt"


def _history_path() -> str:
    configured = os.getenv("GANDALF_CHAT_HISTORY")
    path = Path(configured) if configured else DEFAULT_HISTORY_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


def Main_Brain(text: str) -> str:
    """Generate a response for *text* through the configured reasoning provider."""
    if not text or not text.strip():
        return "Please provide a request."

    try:
        ai = PhindSearch(
            quiet=True,
            filepath=_history_path(),
            is_conversation=None,
        )
        response = ai.chat(text.strip())
        return str(response).strip()
    except Exception as exc:
        # Keep provider failures from crashing the desktop agent.
        print(f"LLM provider error: {exc}")
        return "I couldn't reach the language model right now."
