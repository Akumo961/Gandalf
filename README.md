# Gandalf — Multimodal AI Agent for Voice, Vision & Desktop Automation

> A Python AI-agent project that connects LLM reasoning, speech, computer vision, image generation, and local desktop tools through one modular orchestration layer.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![AI Engineering](https://img.shields.io/badge/Focus-AI%20Engineering-purple)](#ai-engineering)
[![License](https://img.shields.io/badge/License-GPL--3.0-blue)](LICENSE)

## Overview

Gandalf is a hands-on AI engineering project focused on the layer between a language model and real-world computer actions.

The agent accepts natural-language or voice commands, routes them to specialized capabilities, and returns results through text and speech. It combines **LLM reasoning, multimodal perception, tool execution, and operating-system integrations** rather than acting as a simple chat interface.

The project started as a personal desktop assistant and is being progressively refactored toward a more maintainable agent architecture: explicit provider boundaries, configurable integrations, safer side effects, isolated runtime state, and automated quality checks.

## AI engineering

| Area | What Gandalf demonstrates |
| --- | --- |
| **AI agents** | Natural-language commands routed to specialized tools |
| **LLM applications** | Provider-isolated conversational reasoning |
| **Multimodal AI** | Text, speech, camera images, and generated images |
| **Computer vision** | Camera capture and OpenAI-compatible vision inference |
| **Tool integration** | Browser, application, media, system, and productivity actions |
| **Automation safety** | Shell-free process launching and configurable external providers |
| **Concurrency** | Background listener, command loop, monitoring, and scheduling workers |
| **Python engineering** | Modular packages, type hints, runtime isolation, and testable utilities |
| **Cloud/API integration** | HTTP-based AI services with configurable endpoints and bounded timeouts |
| **Developer tooling** | Ruff, pytest, and GitHub Actions quality gates |

## Architecture

```text
                 ┌─────────────────────┐
                 │  Voice / Text Input │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Command Router    │
                 │  & Orchestration    │
                 └──────────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
   ┌────────────┐    ┌────────────┐    ┌──────────────┐
   │ LLM Brain  │    │ Vision     │    │ Desktop      │
   │ Reasoning  │    │ Pipeline   │    │ Tools        │
   └────────────┘    └────────────┘    └──────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Text / Voice Output │
                 └─────────────────────┘
```

The current codebase is organized into capability-focused modules including `Brain`, `Vision`, `Automation`, `TextToSpeech`, `NetHyTechSTT`, `TextToImage`, `Features`, and `Time_Operations`.

## Core capabilities

### LLM reasoning

`Brain/brain.py` isolates the reasoning provider behind `Main_Brain()`. Provider-specific configuration and chat history are kept outside the orchestration layer, making future provider replacement easier.

### Voice interaction

The speech bridge uses Selenium to connect to a browser-based speech-recognition interface and writes recognized commands into `.runtime/input.txt`. The speech endpoint is configurable with `GANDALF_STT_WEBSITE_URL`.

### Computer vision

The local-camera pipeline captures a frame, encodes it, and sends it to an OpenAI-compatible vision endpoint. The endpoint, model, optional API key, and request timeout are configurable through environment variables.

### Desktop automation

The automation layer can open applications and websites, control media/browser actions, inspect system state, and trigger productivity workflows. Model-generated application launches use `subprocess` without a shell rather than executing arbitrary shell strings.

### Image generation

Image generation is isolated behind a small adapter with a configurable endpoint, bounded request timeout, and runtime output directory.

### Speech output

Text-to-speech requests use URL-encoded parameters, explicit request timeouts, temporary audio files, and guaranteed cleanup.

## Configuration

Gandalf keeps provider-specific settings out of source code where practical.

Common variables:

```text
GANDALF_CHAT_HISTORY=.runtime/chat_history.txt
GANDALF_REQUEST_TIMEOUT=30
GANDALF_VISION_ENDPOINT=<OpenAI-compatible vision endpoint>
GANDALF_VISION_MODEL=<vision model>
DEEPINFRA_API_KEY=<optional provider key>
GANDALF_MOBILE_CAMERA_URL=<optional camera stream>
GANDALF_STT_WEBSITE_URL=<speech recognition page>
GANDALF_TTS_ENDPOINT=<TTS endpoint>
GANDALF_TTS_VOICE=Matthew
GANDALF_IMAGE_ENDPOINT=<image generation endpoint>
```

**Never commit real credentials or private endpoints.** Use environment variables or a local `.env` file that remains untracked.

## Project structure

```text
Gandalf/
├── Brain/                 # LLM reasoning adapter
├── Automation/            # Desktop and browser automation
├── Vision/                # Camera and vision-model integrations
├── TextToSpeech/          # Speech synthesis
├── NetHyTechSTT/          # Speech-recognition bridge
├── TextToImage/           # Image-generation adapter
├── Features/              # System and productivity features
├── Time_Operations/       # Scheduling and alarms
├── core/                  # Provider-independent, testable utilities
├── tests/                 # Automated unit tests
├── .github/workflows/     # CI quality gates
├── co_brain.py            # Command orchestration
├── jarvis.py              # Application entry point
├── requirements.txt       # Runtime dependencies
├── requirements-dev.txt   # Development/test dependencies
├── pyproject.toml         # Ruff and pytest configuration
└── LICENSE                # GPL-3.0
```

## Run locally

### Requirements

- Windows
- Python 3.10+
- Microphone for voice features
- Optional camera for vision features
- Chrome/Selenium support for the speech-recognition bridge
- Provider credentials/configuration for the AI services you enable

### Install

```bash
git clone https://github.com/Akumo961/Gandalf.git
cd Gandalf
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run tests

```bash
pytest
```

### Run linting

```bash
ruff check --select F,I,UP,B core tests Brain/brain.py Vision/Vbrain.py Vision/MVbrain.py TextToSpeech/Fast_DF_TTS.py TextToImage/gen_image.py NetHyTechSTT/listen.py Automation/open_App.py Automation/Automation_Brain.py co_brain.py jarvis.py
```

### Start the agent

```bash
python jarvis.py
```

> Gandalf is Windows-oriented and some integrations depend on external services or local hardware. Individual capabilities can be disabled or reconfigured without changing the orchestration layer.

## Engineering roadmap

The project is intentionally being developed as an AI-engineering portfolio rather than presented as a finished commercial product.

- [x] Isolate core AI/provider integrations
- [x] Remove hardcoded personal filesystem paths
- [x] Remove hardcoded mobile-camera address
- [x] Move runtime state outside the repository
- [x] Add shell-free application launching
- [x] Add request timeouts and graceful provider failures
- [x] Add unit-testable core utilities
- [x] Add Ruff + pytest + GitHub Actions quality gate
- [ ] Replace file polling with an in-process event/queue architecture
- [ ] Add structured logging and metrics
- [ ] Add explicit tool schemas and permission policies
- [ ] Add agent evaluation and regression datasets
- [ ] Add integration tests with mocked AI providers
- [ ] Add provider adapters with a common interface

## Security notes

Gandalf can control parts of a local Windows environment. It should therefore be treated as **experimental software**, not as a trusted autonomous computer-control system.

Before using it in a sensitive environment, review:

- tool permissions and destructive actions
- credential handling
- filesystem boundaries
- browser/application control
- prompt-to-tool authorization
- external provider trust and data handling
- logging and retention
- model-generated side effects

The repository does not claim enterprise security, clinical accuracy, or production readiness without additional validation.

## Portfolio positioning

Gandalf is intended to demonstrate practical AI engineering across several layers:

**Model → orchestration → multimodal input → tools → operating-system actions → user feedback**

For an AI Engineer role, the strongest discussion points are the engineering trade-offs: how to isolate providers, constrain tool execution, handle failures, test model-adjacent logic, manage concurrency, and evolve a prototype toward a reliable agent platform.

See [`AI_ENGINEERING.md`](AI_ENGINEERING.md) for the detailed portfolio roadmap and interview preparation notes.

## License

GPL-3.0. See [`LICENSE`](LICENSE).

## Author

**Ali El-Sayed Ali** — `Akumo961`
