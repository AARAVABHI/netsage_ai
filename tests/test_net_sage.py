from src.engine import load_cases, render_diagnosis_prompt, run_diagnosis


def test_load_cases_returns_data():
    cases = load_cases()
    assert len(cases) >= 1
    assert 'case_id' in cases.columns
    assert 'show_outputs' in cases.columns


def test_run_diagnosis_returns_structured_fields():
    case = {
        'case_id': 'NET-001',
        'symptom': 'PC1 cannot reach Server1 in VLAN 30',
        'topology_note': 'Inter-VLAN routing issue',
        'show_outputs': 'GigabitEthernet0/0.30 is administratively down, line protocol is down'
    }

    result = run_diagnosis(case)

    assert set(['root_cause', 'osi_layer', 'confidence', 'evidence', 'next_command', 'fix_steps']).issubset(result.keys())
    assert result['osi_layer'] in {'Layer 1', 'Layer 2', 'Layer 3', 'Layer 4', 'Layer 7'}
    assert result['confidence'] > 0


def test_prompt_contains_case_details():
    case = {
        'symptom': 'Host cannot reach gateway',
        'topology_note': 'Access switch uplink',
        'show_outputs': 'GigabitEthernet0/1 is down',
    }

    prompt = render_diagnosis_prompt(case)

    assert 'Host cannot reach gateway' in prompt
    assert 'Access switch uplink' in prompt
    assert 'GigabitEthernet0/1 is down' in prompt


def test_offline_diagnosis_uses_rule_engine(monkeypatch):
    monkeypatch.delenv('NETSAGE_AI_API_KEY', raising=False)
    result = run_diagnosis({'show_outputs': 'GigabitEthernet0/0.30 is administratively down'})
    assert result['source'] == 'rule_engine'
