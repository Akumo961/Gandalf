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

This makes Gandalf a useful portfolio example for multimodal AI application development.

### 3. AI-to-tool integration

The project connects model-driven interaction to real capabilities such as system inspection, automation, weather, messaging, file creation, image generation, and computer vision.

This is the key AI-engineering concept: **the model produces useful intent, while application code owns the actual side effects.**

### 4. Concurrent application workflows

The application uses Python threads for independent workflows including speech, command processing, scheduling, and system monitoring.

### 5. Modular AI architecture

AI reasoning, vision, speech, automation, and system features are separated into modules. This provides a foundation for replacing individual providers without rewriting the entire application.

## What I would discuss in an AI Engineer interview

### Architecture

> I built Gandalf as a multimodal AI assistant rather than a simple chatbot. The application receives voice or text input, routes the request through an orchestration layer, invokes an LLM when reasoning is required, and dispatches specialized capabilities such as computer vision, image generation, or desktop automation.

### Tool calling

> One of the main engineering challenges is separating language understanding from side effects. The long-term architecture should expose tools with explicit schemas and validate tool arguments before execution.

### Reliability

> An AI system that can control a computer needs stronger safeguards than a conversational application. I therefore treat model output as untrusted input and aim to keep execution logic inside deterministic application code.

### Multimodal AI

> Gandalf combines speech, text, and image inputs with generated responses, which gives me practical experience designing AI applications that operate across modalities.

## Recommended modernization roadmap

The following work would make Gandalf substantially stronger as an AI Engineering portfolio project:

1. **Provider abstraction** — isolate LLM, speech, vision, and image-generation providers behind interfaces.
2. **Structured tool schemas** — replace keyword-heavy routing with typed tool definitions and validated arguments.
3. **FastAPI service layer** — expose the agent through a clean API instead of coupling all orchestration to the desktop process.
4. **Configuration management** — remove hard-coded paths and provider settings; use environment-based configuration.
5. **Automated testing** — unit-test routing, tool validation, integrations, and failure handling.
6. **Evaluation** — create representative prompts and measure routing accuracy, tool-selection accuracy, and response quality.
7. **Observability** — add structured logs and metrics while avoiding sensitive user data.
8. **Safety boundaries** — require confirmation for destructive or high-impact actions.
9. **Containerization** — isolate the API/service components from the Windows desktop integration layer.
10. **Azure deployment path** — add an optional Azure architecture using Azure OpenAI, Azure AI services, managed identity, Key Vault, Application Insights, and GitHub Actions.
11. **CI/CD** — automatically lint, type-check, test, and package the project on every pull request.
12. **Documentation** — document architecture decisions, threat model, evaluation methodology, and deployment design.

## Azure-ready target architecture

The strongest future version of this project would separate the local computer-control agent from a cloud AI service:

```text
                 ┌──────────────────────┐
                 │ Voice / Web Client   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ FastAPI Agent API     │
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

Gandalf is most valuable on a resume when presented as evidence of:

- AI application engineering
- agent/tool orchestration
- multimodal AI integration
- Python software engineering
- API and systems integration
- computer vision
- voice AI
- automation
- reliability and safety thinking

The repository should not be presented as a production enterprise agent until the hardening roadmap is actually implemented and verified.
