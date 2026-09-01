# Gandalf — Multimodal AI Voice Agent & Desktop Automation

> A Python-based AI assistant that combines voice interaction, LLM reasoning, computer vision, image generation, and desktop automation into one extensible agent.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![AI Engineering](https://img.shields.io/badge/Focus-AI%20Engineering-purple)](#ai-engineering-focus)
[![License](https://img.shields.io/badge/License-GPL--3.0-blue)](LICENSE)

## Why this project exists

Gandalf is a hands-on AI engineering project built around a practical question:

**How can an AI assistant understand natural-language requests and safely connect LLM capabilities to real-world computer actions?**

The project explores the engineering layer between an LLM and a user's operating system: speech input/output, intent routing, tool execution, computer vision, image generation, system telemetry, and automation.

This repository is intentionally more than a chatbot. It is an experimental **multimodal agent architecture** with modular integrations for AI and operating-system capabilities.

## Core capabilities

- **Voice interaction** — speech-to-text input and text-to-speech responses.
- **LLM reasoning** — natural-language requests are routed through an LLM-backed reasoning layer.
- **Computer vision** — capture and analyze images from a local camera.
- **Image generation** — generate images from natural-language prompts.
- **Desktop automation** — launch and control supported computer tasks through Python integrations.
- **System awareness** — inspect battery, running applications, audio devices, brightness, and volume.
- **Productivity automation** — alarms, scheduling, weather queries, file creation, and messaging workflows.
- **Modular architecture** — AI, vision, speech, automation, and system features are separated into Python modules.
- **Online/offline handling** — the application checks connectivity before starting network-dependent functionality.

## AI Engineering Focus

The most relevant engineering concepts demonstrated by Gandalf are:

| Area | Implementation focus |
| --- | --- |
| LLM applications | LLM-backed conversational reasoning and intent handling |
| AI agents | Natural-language requests mapped to application capabilities |
| Multimodal AI | Voice + text + image input/output |
| Computer vision | Local image capture and vision analysis |
| Tool integration | AI-connected automation functions |
| AI orchestration | Central routing layer connecting AI to tools |
| Python engineering | Modular packages and feature-specific components |
| Concurrency | Threaded speech, reasoning, monitoring, and scheduling workflows |
| System integration | Windows APIs and desktop/device controls |

## Architecture

At a high level, Gandalf follows this flow:

```text
Voice / Text Input
        │
        ▼
Speech & Input Layer
        │
        ▼
Intent / Command Router
        │
        ├──────────────► LLM Reasoning
        │                     │
        │                     ▼
        │               Natural-language response
        │
        ├──────────────► Computer Vision
        ├──────────────► Image Generation
        ├──────────────► Desktop Automation
        ├──────────────► System Controls
        └──────────────► Productivity Integrations
                              │
                              ▼
                    Voice / UI Response
```

The current implementation is organized around modules such as `Brain`, `Vision`, `Automation`, `TextToSpeech`, `NetHyTechSTT`, `Features`, and `Time_Operations`.

## Example interactions

```text
"Jarvis, what can you see?"
        → capture an image
        → send it through the vision layer
        → return an AI-generated description
        → speak the result
```

```text
"Generate an image of a futuristic city"
        → extract the generation prompt
        → call the image-generation integration
        → create the requested image
```

```text
"Check the volume level"
        → route the command
        → query the Windows audio subsystem
        → return the current level
```

## Project structure

```text
Gandalf/
├── Brain/                 # LLM reasoning layer
├── Automation/            # Desktop automation and command execution
├── Vision/                # Computer-vision integrations
├── TextToSpeech/          # Speech synthesis
├── NetHyTechSTT/          # Speech recognition/input
├── Features/              # System and productivity features
├── Time_Operations/       # Scheduling and alarm logic
├── Weather_Check/         # Weather integration
├── TextToImage/           # Image-generation integration
├── Data/                  # Dialog and application data
├── jarvis.py              # Application entry point
├── co_brain.py            # Input routing and orchestration
├── requirements.txt       # Python dependencies
└── LICENSE                # GPL-3.0 license
```

## Running locally

### Requirements

- Windows
- Python 3.10+
- A working microphone for voice interaction
- Optional camera for vision features
- Internet access for network-backed AI/integration features
- Credentials/configuration required by the external AI providers used by the selected modules

### Install

```bash
git clone https://github.com/Akumo961/Gandalf.git
cd Gandalf
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Start

```bash
python jarvis.py
```

> Some integrations are Windows-specific and may require additional system configuration or provider credentials.

## Engineering notes

Gandalf began as a personal desktop assistant and has evolved into a practical exploration of AI-agent engineering. The repository intentionally contains integrations with operating-system capabilities rather than limiting the application to text generation.

The next engineering direction is to make the agent architecture more production-oriented: explicit tool schemas, provider abstraction, configuration through environment variables, structured logging, automated tests, safer tool execution, evaluation of LLM behavior, and clearer separation between model reasoning and side effects.

See [`AI_ENGINEERING.md`](AI_ENGINEERING.md) for the portfolio-oriented engineering roadmap and interview talking points.

## Security considerations

Gandalf can interact with the local operating system. Treat it as experimental software and run it with appropriate permissions.

Before using the project with sensitive environments, review and harden:

- tool permissions and command execution
- credential management
- filesystem access
- external integrations
- prompt/command validation
- logging of user input and generated output
- model-generated actions

The project does **not** claim to be production-safe or enterprise-secure without additional hardening and validation.

## Status

**Portfolio project / active engineering work.**

The project demonstrates practical AI-agent integration and is being modernized toward a cleaner, testable, provider-independent architecture.

## License

GPL-3.0. See [`LICENSE`](LICENSE).

## Author

**Ali El-Sayed Ali (Akumo961)**

GitHub: https://github.com/Akumo961
