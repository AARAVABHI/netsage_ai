# NetSage AI

NetSage AI is an AI-assisted network diagnostic platform for Cisco Packet Tracer labs and educational networking environments. It analyzes network symptoms and Cisco CLI output, identifies likely configuration faults, and recommends safe remediation steps for review by a network engineer or student.

## What the System Does

NetSage AI supports the network troubleshooting workflow from diagnosis to human approval:

1. Loads a structured troubleshooting case from the project dataset.
2. Displays the symptom, topology context, severity, and captured Cisco command output.
3. Checks the output against deterministic diagnostic rules for known network issues.
4. Optionally sends the case to an AI model for additional analysis.
5. Produces a structured diagnosis containing the root cause, OSI layer, confidence score, evidence, next command, and recommended fix steps.
6. Presents the recommendation through a Streamlit dashboard.
7. Requires the operator to approve, edit, or reject the proposed remediation.

The platform does not automatically execute network commands. Human review remains mandatory before any remediation is considered for deployment.

## Key Capabilities

- Detects common interface, VLAN, trunk, routing, ACL, and DHCP issues.
- Uses deterministic rules for transparent and repeatable checks.
- Supports AI-based diagnosis through an OpenAI-compatible API provider.
- Uses `Qwen/Qwen2.5-7B-Instruct` when configured for Hugging Face.
- Validates AI responses before displaying them.
- Falls back to the local rule engine when the AI service is unavailable.
- Provides a human-in-the-loop approval workflow.
- Supports audit documentation for approvals, overrides, and false positives.

## Project Structure

```text
.
|-- app.py                         Streamlit deployment entrypoint
|-- config/system_config.json      Application configuration
|-- data/cases.csv                 Network troubleshooting cases
|-- docs/model_audit_log.md        Audit and review documentation
|-- prompts/diagnose_prompt.md     AI diagnosis instructions and output schema
|-- src/app.py                     Streamlit dashboard implementation
|-- src/checker.py                 Deterministic diagnostic rules
|-- src/engine.py                  Case loading and AI orchestration
|-- tests/test_net_sage.py         Automated tests
|-- requirements.txt               Python dependencies
`-- PROJECT_SUMMARY.md              Overall project summary
```

## Local Setup

From the project directory, install the dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run app.py
```

Run the tests:

```bash
pytest -q
```

## Enable AI Diagnosis

Without an API token, the application uses the deterministic rule engine. To enable AI diagnosis locally, configure the following environment variables:

```dotenv
HUGGINGFACEHUB_API_TOKEN=your-real-token
NETSAGE_AI_MODEL=Qwen/Qwen2.5-7B-Instruct
NETSAGE_AI_BASE_URL=https://router.huggingface.co/v1
```

The application also accepts `NETSAGE_AI_API_KEY` for compatibility with other OpenAI-compatible providers.

Never commit real API tokens to source control. The token should be stored securely in the deployment platform's secret manager.

## Streamlit Cloud Deployment

1. Push the project to a GitHub repository.
2. Open Streamlit Community Cloud and create a new application.
3. Select the repository and branch.
4. Set the main file to `app.py`.
5. Add the following values under the application's secrets settings:

```toml
HUGGINGFACEHUB_API_TOKEN = "your-real-token"
NETSAGE_AI_MODEL = "Qwen/Qwen2.5-7B-Instruct"
NETSAGE_AI_BASE_URL = "https://router.huggingface.co/v1"
```

6. Deploy the application.

After deployment, Streamlit will provide a public URL that can be shared with users.

## Safety and Reliability

NetSage AI is designed as a decision-support tool. Its recommendations should be reviewed against the actual network topology and device configuration before use. The deterministic checker, structured output validation, and human approval gate help reduce the risk of applying incorrect or destructive commands.

## Documentation

- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - overall project summary
- [docs/model_audit_log.md](docs/model_audit_log.md) - audit guidance
- [prompts/diagnose_prompt.md](prompts/diagnose_prompt.md) - AI prompt contract
