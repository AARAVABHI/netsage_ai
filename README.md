# NetSage AI

NetSage AI is a hybrid diagnostic platform for Cisco Packet Tracer and network troubleshooting labs. It combines deterministic rule checks with structured LLM prompts and a human-in-the-loop approval gate.

## Project Goal

The system helps network engineers and students identify root causes from CLI output, explain the likely OSI layer involved, and validate remediation before deployment.

## Architecture

- Data layer: `data/cases.csv`
- Diagnostic engine: `src/checker.py`, `src/engine.py`
- Human oversight dashboard: `src/app.py`
- Prompt templates: `prompts/diagnose_prompt.md`
- Documentation and audit notes: `docs/model_audit_log.md`
