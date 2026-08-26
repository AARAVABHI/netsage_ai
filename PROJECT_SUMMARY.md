# NetSage AI Project Summary

## Overview

NetSage AI is an automated network diagnostic and remediation platform designed for Cisco Packet Tracer and educational lab troubleshooting. It builds on a hybrid architecture combining deterministic rule checking with structured diagnostic prompts and a required human oversight gate.

## Problem Addressed

The system addresses the significant challenge of manual multi-layer troubleshooting in network labs, where engineers must inspect verbose CLI output, determine likely root causes, and validate commands before executing remediation.

## Core Features

- Deterministic rule-based detection for common network faults
- Structured diagnosis output with root cause, OSI layer, confidence, evidence, recommended command, and fix steps
- Human-in-the-loop approval workflow in the Streamlit dashboard
- Audit logging for overrides, approvals, and false positives
- Dataset-driven testing based on sample Packet Tracer cases

## Architecture

The project is organized into four functional tiers:

1. Data Tier
   - `data/cases.csv` contains problem scenarios and sample CLI outputs.

2. Diagnostic Core
   - `src/checker.py` detects known error patterns.
   - `src/engine.py` orchestrates case loading and diagnosis generation.
   - `prompts/diagnose_prompt.md` defines the prompt contract and JSON schema.

3. HITL Gate
   - `src/app.py` provides the Streamlit interface for case review and approval decisions.

4. Audit & Documentation
   - `docs/model_audit_log.md` tracks system review and override records.

## Main Use Case

A network engineer or student selects a case such as NET-001, reviews the show outputs, and receives a structured diagnosis indicating the likely issue and exact remediation sequence. The operator then chooses to approve, edit, or reject the fix before deployment.

## Deployment Readiness

The solution is designed to run locally and can also be deployed to a Streamlit-hosted environment. It uses simple file-based configuration, CSV-based data, and standard Python packages, which makes it portable and easy to deploy.

## Files Added

- `README.md`
- `requirements.txt`
- `config/system_config.json`
- `data/cases.csv`
- `prompts/diagnose_prompt.md`
- `src/checker.py`
- `src/engine.py`
- `src/app.py`
- `docs/model_audit_log.md`
- `tests/test_net_sage.py`

## Run Instructions

1. Install dependencies: `pip install -r requirements.txt`
2. Launch the app: `streamlit run src/app.py`
3. Run tests: `pytest -q`
