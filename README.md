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
<<<<<<< HEAD

## Quick Start

1. Create a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the dashboard locally:
   `streamlit run app.py`
4. Run tests:
   `pytest -q`

## Streamlit Deployment

This app is ready for Streamlit Cloud and other public hosting environments.

### Required for deployment

- Keep the app entrypoint as `app.py` at the repository root.
- Ensure all dependencies are listed in `requirements.txt`.
- Use the included `.streamlit/config.toml` for deployment-friendly server settings.

### Deploy to Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Open Streamlit Cloud.
3. Select the repo and branch.
4. Set the main file to `app.py`.
5. Deploy.

The dashboard will then be publicly accessible to anyone with the deployment link.

## Deployment Notes

This project is designed to run in a local deployment or hosted Streamlit environment. The app uses file-based data, rule checks, and structured JSON outputs so it remains deterministic and auditable.

## Enable AI Diagnosis

The app uses the deterministic checker when no key is configured. To send cases to the AI model, add these variables in Streamlit Cloud under **Settings > Secrets**:

```toml
NETSAGE_AI_API_KEY = "your-api-key"
NETSAGE_AI_MODEL = "gpt-4o-mini"
```

Never commit an API key to GitHub. With the key configured, the dashboard sends the case symptom, topology note, and CLI output to the model using `prompts/diagnose_prompt.md`, requests strict JSON, validates the response, and falls back to the rule engine if the model is unavailable or returns invalid data.
=======
>>>>>>> a7b064b08fc0eb6a912d598bc7823bac0b504c21
