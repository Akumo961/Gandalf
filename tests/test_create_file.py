from pathlib import Path

import pytest

from Features.create_file import _safe_filename, get_file_extension


def test_get_file_extension():
    assert get_file_extension("create a python file named demo") == ".py"
    assert get_file_extension("create a markdown file") == ".md"
    assert get_file_extension("create a mystery file") == ""


def test_created_filename_cannot_escape_runtime(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    destination = _safe_filename("create text file named ../../outside", ".txt")
    assert destination.parent == (Path(".runtime").resolve())
    assert destination.name == "outside.txt"


def test_unknown_extension_is_rejected():
    with pytest.raises(ValueError):
        _safe_filename("create something", "")
