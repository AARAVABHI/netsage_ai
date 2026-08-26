import json
from pathlib import Path
from typing import Dict, List

import pandas as pd

from src.checker import build_diagnostic_from_checker

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / 'data' / 'cases.csv'
PROMPT_PATH = ROOT / 'prompts' / 'diagnose_prompt.md'


def load_cases() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def load_prompt_template() -> str:
    return PROMPT_PATH.read_text(encoding='utf-8')


def run_diagnosis(case: Dict) -> Dict:
    output = build_diagnostic_from_checker(case.get('show_outputs', ''))

    if 'root_cause' in output and 'osi_layer' in output:
        output['case_id'] = case.get('case_id', 'UNKNOWN')
        output['symptom'] = case.get('symptom', '')
        output['topology_note'] = case.get('topology_note', '')
        output['confidence'] = float(output.get('confidence', 0.0))
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
