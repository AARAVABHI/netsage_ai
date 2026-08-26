from src.engine import load_cases, run_diagnosis


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
