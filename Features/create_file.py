"""Safe, voice-driven file creation utility."""

from __future__ import annotations

from pathlib import Path


EXTENSIONS = {
    "python file": ".py",
    "java file": ".java",
    "text file": ".txt",
    "html file": ".html",
    "css file": ".css",
    "javascript file": ".js",
    "json file": ".json",
    "xml file": ".xml",
    "csv file": ".csv",
    "markdown file": ".md",
    "yaml file": ".yaml",
    "image file": ".jpg",
    "video file": ".mp4",
    "audio file": ".mp3",
    "pdf file": ".pdf",
    "word file": ".docx",
    "excel file": ".xlsx",
    "powerpoint file": ".pptx",
    "zip file": ".zip",
    "tar file": ".tar",
}
RUNTIME_DIR = Path(".runtime")


def get_file_extension(text: str) -> str:
    """Return the first supported extension mentioned in a command."""
    normalized = text.lower()
    for file_type, extension in EXTENSIONS.items():
        if file_type in normalized:
            return extension
    return ""


def update_text(text: str) -> str:
    """Remove the supported file-type phrase from a command."""
    normalized = text.lower()
    for file_type in EXTENSIONS:
        normalized = normalized.replace(file_type, "")
    return normalized


def _safe_filename(command: str, extension: str) -> Path:
    if not extension:
        raise ValueError("unsupported file type")

    name = command.replace("named", "").replace("with name", "")
    name = name.replace("create", "").strip()
    if not name:
        name = "demo"

    # Keep the feature intentionally limited to a single filename, never a path.
    filename = Path(name).name.replace("..", "")
    if not filename:
        filename = "demo"
    if Path(filename).suffix.lower() != extension:
        filename = f"{filename}{extension}"

    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    destination = (RUNTIME_DIR / filename).resolve()
    runtime_root = RUNTIME_DIR.resolve()
    if destination.parent != runtime_root:
        raise ValueError("file name must not contain a directory path")
    return destination


def create_file(text: str) -> Path:
    """Create a file under `.runtime` and return its path."""
    extension = get_file_extension(text)
    destination = _safe_filename(update_text(text), extension)
    destination.touch(exist_ok=True)
    print(f"Created {destination}")
    return destination
