# Gandalf Architecture

## Design goal

Gandalf separates **reasoning**, **orchestration**, **capabilities**, and **side effects** so an AI provider can change without rewriting every tool integration.

```text
Input
  │
  ├── Speech recognition
  └── Text/runtime input
          │
          ▼
   Command orchestration
          │
    ┌─────┼─────────────┐
    ▼     ▼             ▼
   LLM  Vision        Tools
    │     │             │
    └─────┴─────────────┘
          │
          ▼
     User feedback
```

## Boundaries

- `Brain/` — LLM provider adapter.
- `Vision/` — camera capture and vision inference.
- `TextToSpeech/` — speech synthesis provider adapter.
- `NetHyTechSTT/` — speech-recognition bridge.
- `Automation/` — browser, application, and media side effects.
- `Features/` — system and productivity capabilities.
- `core/` — provider-independent logic that can be unit tested without hardware.
- `co_brain.py` — command dispatch and coordination.
- `jarvis.py` — process lifecycle and background workers.

## Runtime state

Ephemeral state is kept under `.runtime/` and excluded from version control. Provider configuration is supplied through environment variables rather than hardcoded user paths, phone numbers, camera addresses, or credentials.

## Current trade-offs

The current command handoff still uses a small file-based interface because it preserves compatibility with the existing speech-recognition bridge. The roadmap is to replace this with an in-process queue/event bus and explicit tool contracts.

## Reliability direction

The next architectural improvements are:

1. Common provider interfaces for LLM, vision, TTS, and image generation.
2. Typed tool schemas and a permission policy before side effects.
3. Structured logging with sensitive-data filtering.
4. Mockable provider clients and integration tests.
5. Evaluation datasets for routing, tool selection, and model responses.
6. Cancellation and graceful shutdown for long-running workers.
