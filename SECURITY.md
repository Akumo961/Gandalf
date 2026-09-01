# Security Notes

Gandalf is a desktop-control AI agent. Treat model output as **untrusted input** and require additional controls before deploying it in a sensitive environment.

## Implemented protections

- Runtime state is kept out of the tracked source tree.
- Personal messaging records and hardcoded phone numbers were removed.
- Application launching uses `subprocess` without a shell.
- Provider endpoints and credentials are configurable through environment variables.
- Network calls use bounded timeouts and graceful failure handling.
- Voice-created files are constrained to the `.runtime` directory.
- Mobile-camera addresses are no longer hardcoded.

## Remaining risks

The project can still perform consequential desktop actions through PyAutoGUI and other integrations. A malicious prompt, compromised model/provider, or unexpected speech-recognition result could therefore cause unintended actions.

Before production use, add:

- explicit tool allowlists and per-tool permissions
- confirmation for destructive or externally visible actions
- authentication/authorization if exposed beyond the local user
- input/output redaction and structured security logging
- dependency and supply-chain scanning
- integration tests for dangerous tool paths
- network egress restrictions where appropriate
- a kill switch and graceful cancellation

## Secrets

Never commit API keys, phone numbers, private camera URLs, access tokens, or personal message logs. Use environment variables or an approved local secret manager.
