"""Speech-recognition bridge used by the desktop agent."""

from __future__ import annotations

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


STT_WEBSITE_URL = os.getenv(
    "GANDALF_STT_WEBSITE_URL",
    "https://allorizenproject1.netlify.app/",
)
RUNTIME_INPUT = Path(".runtime") / "input.txt"


def _build_driver() -> webdriver.Chrome:
    """Create a headless Chrome driver using Selenium Manager."""
    options = Options()
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)


def listen() -> None:
    """Stream recognized speech into the local runtime input file."""
    RUNTIME_INPUT.parent.mkdir(parents=True, exist_ok=True)
    driver = _build_driver()

    try:
        driver.get(STT_WEBSITE_URL)
        start_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "startButton"))
        )
        start_button.click()
        print("Listening for commands...")

        last_text = ""
        while True:
            output = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "output"))
            )
            current_text = output.text.strip().lower()
            if current_text and current_text != last_text:
                last_text = current_text
                RUNTIME_INPUT.write_text(current_text, encoding="utf-8")
                print(f"User: {current_text}")
    except KeyboardInterrupt:
        print("Speech recognition stopped.")
    except Exception as exc:
        print(f"Speech recognition error: {exc}")
    finally:
        driver.quit()
