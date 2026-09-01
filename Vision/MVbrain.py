"""Mobile/DroidCam capture adapter and vision-model integration."""

from __future__ import annotations

import base64
import os
from pathlib import Path

import cv2
import requests


CAMERA_URL = os.getenv("GANDALF_MOBILE_CAMERA_URL", "")
VISION_ENDPOINT = os.getenv(
    "GANDALF_VISION_ENDPOINT",
    "https://api.deepinfra.com/v1/openai/chat/completions",
)
VISION_MODEL = os.getenv("GANDALF_VISION_MODEL", "llava-hf/llava-1.5-7b-hf")
REQUEST_TIMEOUT = float(os.getenv("GANDALF_REQUEST_TIMEOUT", "30"))


def capture_image_and_save(image_path: str = "captured_image.png") -> bool:
    """Capture one frame from the configured mobile camera stream."""
    if not CAMERA_URL:
        print("Mobile camera is not configured. Set GANDALF_MOBILE_CAMERA_URL.")
        return False

    output = Path(image_path)
    cap = cv2.VideoCapture(CAMERA_URL)
    if not cap.isOpened():
        print("Error: could not open the configured mobile camera.")
        return False

    try:
        ok, frame = cap.read()
        if not ok:
            print("Error: could not capture a mobile-camera frame.")
            return False
        output.parent.mkdir(parents=True, exist_ok=True)
        return bool(cv2.imwrite(str(output), frame))
    finally:
        cap.release()
        cv2.destroyAllWindows()


def encode_image_to_base64(image_path: str) -> str:
    return base64.b64encode(Path(image_path).read_bytes()).decode("utf-8")


def mobile_vision_brain(encoded_image: str) -> str:
    """Send the mobile-camera frame to the configured OpenAI-compatible endpoint."""
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
        print(f"Mobile vision provider error: {exc}")
        return "I couldn't analyze the mobile-camera image right now."
