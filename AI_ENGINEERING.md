# Gandalf — AI Engineering Portfolio Guide

## Positioning

Gandalf is a **multimodal AI voice agent and desktop automation system** implemented in Python.

The project demonstrates the engineering work required to connect AI models to real software capabilities rather than treating an LLM as an isolated chat interface.

## Engineering problems explored

### 1. Natural-language command routing

User requests enter through voice/text input and are routed according to intent. The orchestration layer decides whether a request should go to the LLM reasoning layer or to a specialized tool/integration.

### 2. Multimodal interaction

The application combines:

- speech recognition
- text input
- text-to-speech
- image input
- computer vision
- image generation

This makes Gandalf a practical portfolio example for multimodal AI application development.

### 3. AI-to-tool integration

The project connects model-driven interaction to real capabilities such as system inspection, automation, weather, messaging, file creation, image generation, and computer vision.

The core engineering boundary is: **model/provider code produces intent and content; deterministic application code owns side effects.**

### 4. Concurrent application workflows

The application uses Python threads for independent workflows including speech, command processing, scheduling, and system monitoring.

### 5. Modular AI architecture

AI reasoning, vision, speech, automation, and system features are separated into modules. Provider endpoints are now configurable so individual integrations can evolve independently.

## Improvements completed

The repository has been actively modernized without pretending the prototype is production-ready:

- Removed hardcoded personal filesystem paths.
- Removed a hardcoded mobile-camera address.
- Removed hardcoded WhatsApp recipient data and committed messaging history.
- Moved runtime state to `.runtime/` and added repository ignore rules.
- Added configurable provider endpoints and model settings.
- Added bounded network timeouts and graceful provider failures.
- Replaced shell-based application execution with `subprocess` calls that do not invoke a shell.
- Constrained voice-created files to the runtime directory.
- Added pure, unit-testable command validation helpers.
- Added pytest coverage for command normalization and file-boundary validation.
- Added Ruff configuration and a GitHub Actions quality gate.
- Added architecture and security documentation.

## What I would discuss in an AI Engineer interview

### Architecture

> I built Gandalf as a multimodal AI assistant rather than a simple chatbot. The application receives voice or text input, routes the request through an orchestration layer, invokes an LLM when reasoning is required, and dispatches specialized capabilities such as computer vision, image generation, or desktop automation.

### Tool execution

> A key engineering concern is separating language understanding from side effects. The current implementation keeps execution in deterministic Python functions and has started moving provider configuration and input validation outside the orchestration layer.

### Reliability

> An AI system that can control a computer needs stronger safeguards than a conversational application. I treat model output and speech-recognition output as untrusted input, use bounded network calls, and avoid shell execution for application launching.

### Multimodal AI

> Gandalf combines speech, text, and image inputs with generated responses, giving me practical experience integrating multiple AI modalities into one application.

## Next engineering priorities

The remaining work that would make Gandalf substantially stronger is:

1. **Provider interfaces** — define common interfaces for LLM, speech, vision, and image-generation adapters.
2. **Structured tool schemas** — replace keyword-heavy routing with typed tool definitions and validated arguments.
3. **Event-driven runtime** — replace file polling with an in-process queue/event bus.
4. **FastAPI service layer** — expose the agent through a clean API while keeping Windows-only tools in a separate local worker.
5. **Evaluation** — create representative prompts and measure routing accuracy, tool-selection accuracy, and response quality.
6. **Observability** — add structured logs and metrics while avoiding sensitive user data.
7. **Safety boundaries** — require confirmation for destructive or externally visible actions.
8. **Integration testing** — mock AI providers and test dangerous tool paths without controlling a real desktop.
9. **Containerization** — isolate API/service components from the Windows desktop integration layer.
10. **Optional Azure deployment** — use Azure OpenAI, managed identity, Key Vault, Application Insights, and GitHub Actions only when actually implemented.

## Azure-ready target architecture

A stronger future version can separate the local computer-control agent from a cloud AI service:

```text
                 ┌──────────────────────┐
                 │ Voice / Web Client   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ FastAPI Agent API    │
                 │ Auth + Validation    │
                 └──────────┬───────────┘
                            │
                    ┌───────▼────────┐
                    │ Agent Router   │
                    │ Tool Selection │
                    └───────┬────────┘
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼
   ┌────────────┐    ┌──────────────┐   ┌──────────────┐
   │ Azure      │    │ Tool Layer   │   │ Vision /     │
   │ OpenAI     │    │ validation   │   │ Speech       │
   └────────────┘    └──────┬───────┘   └──────────────┘
                             │
                             ▼
                     ┌──────────────┐
                     │ Desktop /    │
                     │ External APIs│
                     └──────────────┘

        Observability → Application Insights
        Secrets       → Azure Key Vault
        CI/CD         → GitHub Actions
        Identity      → Managed Identity / Entra ID
```

This target architecture is a **roadmap**, not a claim that all Azure components are currently implemented.

## Portfolio value

Gandalf is strongest on a resume as evidence of:

- AI application engineering
- agent/tool orchestration
- multimodal AI integration
- Python software engineering
- API and systems integration
- computer vision
- voice AI
- automation
- reliability and safety engineering

The repository should not be presented as a production enterprise agent until the remaining hardening, evaluation, and integration work is actually implemented and verified.
