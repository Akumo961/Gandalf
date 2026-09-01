"""Pure command-normalization helpers used by the agent."""

from __future__ import annotations

import re


_TIME_MARKER = re.compile(r"\b([1-9]):")


def normalize_spoken_time(text: str) -> str:
    """Normalize common speech-to-text time markers such as ``7:30``."""
    value = text.replace(" p.m.", "PM").replace(" a.m.", "AM")
    return _TIME_MARKER.sub(lambda match: f"0{match.group(1)}:", value)


def parse_percentage(text: str) -> int:
    """Parse a percentage command value and reject values outside 0..100."""
    value = text.strip().replace("%", "")
    if not value.isdigit():
        raise ValueError("percentage must be an integer")
    number = int(value)
    if not 0 <= number <= 100:
        raise ValueError("percentage must be between 0 and 100")
    return number
