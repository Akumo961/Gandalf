import pytest

from core.command_utils import normalize_spoken_time, parse_percentage


def test_normalize_spoken_time():
    assert normalize_spoken_time("set alarm at 7:30 p.m.") == "set alarm at 07:30PM"
    assert normalize_spoken_time("set alarm at 12:15 a.m.") == "set alarm at 12:15AM"


def test_parse_percentage_accepts_valid_values():
    assert parse_percentage("0") == 0
    assert parse_percentage("50%") == 50
    assert parse_percentage("100") == 100


@pytest.mark.parametrize("value", ["-1", "101", "abc", "50.5"])
def test_parse_percentage_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        parse_percentage(value)
