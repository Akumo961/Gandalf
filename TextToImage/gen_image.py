"""Image-generation adapter."""

from __future__ import annotations

import os
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image


IMAGE_ENDPOINT = os.getenv(
    "GANDALF_IMAGE_ENDPOINT",
    "https://api.airforce/v1/imagine2",
)
REQUEST_TIMEOUT = float(os.getenv("GANDALF_REQUEST_TIMEOUT", "60"))
OUTPUT_PATH = Path(".runtime") / "generated_image.png"


def generate_image(text: str, output_path: str | Path = OUTPUT_PATH) -> bool:
    """Generate an image and save it locally.

    The endpoint is configurable so the agent is not permanently coupled to a
    single third-party provider.
    """
    prompt = text.strip()
    if not prompt:
        return False

    try:
        response = requests.get(
            IMAGE_ENDPOINT,
            params={"prompt": prompt},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination)
        print(f"Image saved to {destination}")
        return True
    except (requests.RequestException, OSError, ValueError) as exc:
        print(f"Image generation error: {exc}")
        return False
