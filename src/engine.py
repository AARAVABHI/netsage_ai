import json
import os
from pathlib import Path
from typing import Dict

import pandas as pd

from src.checker import build_diagnostic_from_checker

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / 'data' / 'cases.csv'
PROMPT_PATH = ROOT / 'prompts' / 'diagnose_prompt.md'


def load_cases() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def load_prompt_template() -> str:
    return PROMPT_PATH.read_text(encoding='utf-8')


def render_diagnosis_prompt(case: Dict) -> str:
    prompt = load_prompt_template()
    replacements = {
        '{symptom}': str(case.get('symptom', '')),
        '{topology_note}': str(case.get('topology_note', '')),
        '{show_outputs}': str(case.get('show_outputs', '')),
    }
    for placeholder, value in replacements.items():
        prompt = prompt.replace(placeholder, value)
    return prompt


def _validate_model_result(result: Dict, case: Dict) -> Dict:
    required_fields = {
        'root_cause', 'osi_layer', 'confidence', 'evidence',
        'next_command', 'fix_steps'
    }
    missing_fields = required_fields.difference(result)
    if missing_fields:
        raise ValueError(f'Model response is missing fields: {sorted(missing_fields)}')

    confidence = float(result['confidence'])
    if not 0 <= confidence <= 1:
        raise ValueError('Model confidence must be between 0 and 1')
    if not isinstance(result['evidence'], list) or not isinstance(result['fix_steps'], list):
        raise ValueError('Model evidence and fix_steps must be JSON arrays')

    result['confidence'] = confidence
    result['case_id'] = case.get('case_id', 'UNKNOWN')
    result['symptom'] = case.get('symptom', '')
    result['topology_note'] = case.get('topology_note', '')
    result['source'] = 'ai_model'
    return result


def run_ai_diagnosis(case: Dict) -> Dict:
    api_key = os.getenv('NETSAGE_AI_API_KEY')
    if not api_key:
        raise RuntimeError('NETSAGE_AI_API_KEY is not configured')

    try:
        from openai import OpenAI
    except ImportError as error:
        raise RuntimeError('Install the openai package to use AI diagnosis') from error

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv('NETSAGE_AI_MODEL', 'gpt-4o-mini'),
        temperature=0,
        response_format={'type': 'json_object'},
        messages=[
            {
                'role': 'system',
                'content': 'Return only valid JSON matching the requested diagnostic schema.',
            },
            {'role': 'user', 'content': render_diagnosis_prompt(case)},
        ],
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError('Model returned an empty response')
    return _validate_model_result(json.loads(content), case)


def run_diagnosis(case: Dict, use_ai: bool = True) -> Dict:
    if use_ai and os.getenv('NETSAGE_AI_API_KEY'):
        try:
            return run_ai_diagnosis(case)
        except (ValueError, RuntimeError, json.JSONDecodeError) as error:
            fallback = build_diagnostic_from_checker(case.get('show_outputs', ''))
            fallback['diagnostic_warning'] = f'AI diagnosis failed; rule engine used: {error}'
            output = fallback
        except Exception as error:
            fallback = build_diagnostic_from_checker(case.get('show_outputs', ''))
            fallback['diagnostic_warning'] = f'AI service unavailable; rule engine used: {error}'
            output = fallback
    else:
        output = build_diagnostic_from_checker(case.get('show_outputs', ''))

    if 'root_cause' in output and 'osi_layer' in output:
        output['case_id'] = case.get('case_id', 'UNKNOWN')
        output['symptom'] = case.get('symptom', '')
        output['topology_note'] = case.get('topology_note', '')
        output['confidence'] = float(output.get('confidence', 0.0))
        output.setdefault('source', 'rule_engine')
        return output

    return {
        'case_id': case.get('case_id', 'UNKNOWN'),
        'root_cause': 'No issue resolved',
        'osi_layer': 'Layer 3',
        'confidence': 0.0,
        'evidence': ['No diagnostic evidence found'],
        'next_command': 'show running-config',
        'fix_steps': ['Inspect the output manually.']
    }


def generate_summary(case: Dict) -> str:
    diagnosis = run_diagnosis(case)
    return json.dumps(diagnosis, indent=2)
