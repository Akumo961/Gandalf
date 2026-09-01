"""Local camera capture and vision-model integration."""

from __future__ import annotations

import base64
import os
from pathlib import Path

import cv2
import requests


VISION_ENDPOINT = os.getenv(
    "GANDALF_VISION_ENDPOINT",
    "https://api.deepinfra.com/v1/openai/chat/completions",
)
VISION_MODEL = os.getenv(
    "GANDALF_VISION_MODEL",
    "llava-hf/llava-1.5-7b-hf",
)
REQUEST_TIMEOUT = float(os.getenv("GANDALF_REQUEST_TIMEOUT", "30"))


def capture_image_and_save(image_path: str = "captured_image.png") -> bool:
    """Capture one frame from the default local camera."""
    output = Path(image_path)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: could not open the default camera.")
        return False

    try:
        ok, frame = cap.read()
        if not ok:
            print("Error: could not capture a camera frame.")
            return False
        output.parent.mkdir(parents=True, exist_ok=True)
        return bool(cv2.imwrite(str(output), frame))
    finally:
        cap.release()
        cv2.destroyAllWindows()


def encode_image_to_base64(image_path: str) -> str:
    """Encode a local image for an OpenAI-compatible vision endpoint."""
    return base64.b64encode(Path(image_path).read_bytes()).decode("utf-8")


def vision_brain(encoded_image: str) -> str:
    """Ask the configured vision model to describe the supplied image."""
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("DEEPINFRA_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encoded_image}"},
                    },
                    {"type": "text", "text": "Describe what is visible in this image."},
                ],
            }
        ],
    }

    try:
        response = requests.post(
            VISION_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return str(data["choices"][0]["message"]["content"]).strip()
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"Vision provider error: {exc}")
        return "I couldn't analyze the image right now."
