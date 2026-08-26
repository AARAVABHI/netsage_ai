import re
from typing import Dict, List


def detect_issue(show_outputs: str) -> Dict:
    text = (show_outputs or '').lower()

    patterns = {
        'administratively_down': re.compile(r'administratively down|administratively shutdown', re.I),
        'vlan_down': re.compile(r'vlan\s*\d+\s+is\s+down|interface.*vlan.*down', re.I),
        'access_list_block': re.compile(r'permit ip any any|deny tcp any any eq 22|acl.*deny', re.I),
        'ipv4_route_missing': re.compile(r'no route to|ip route.*unreachable|gateway.*unreachable', re.I),
        'dhcp_issue': re.compile(r'169\.254\.|dhcp.*failed|no dhcp lease', re.I),
        'trunk_mismatch': re.compile(r'trunk|encapsulation dot1q|switchport mode access', re.I),
    }

    for issue_name, pattern in patterns.items():
        if pattern.search(text):
            details = {
                'issue': issue_name,
                'detected': True,
                'match_text': pattern.search(show_outputs or '').group(0) if (show_outputs or '') else '',
            }
            return details

    return {'issue': 'no_rule_match', 'detected': False, 'match_text': ''}


def build_diagnostic_from_checker(show_outputs: str) -> Dict:
    issue = detect_issue(show_outputs)
    if not issue['detected']:
        return {
            'root_cause': 'No deterministic rule match; manual review recommended',
            'osi_layer': 'Layer 3',
            'confidence': 0.4,
            'evidence': ['No known pattern matched the provided output'],
            'next_command': 'show running-config',
            'fix_steps': ['Review the interface and routing configuration manually.']
        }

    if issue['issue'] == 'administratively_down':
        return {
            'root_cause': 'Interface or sub-interface is administratively shut down',
            'osi_layer': 'Layer 1',
            'confidence': 0.94,
            'evidence': [issue['match_text'] or 'Interface status indicates administrative shutdown'],
            'next_command': 'show interfaces status',
            'fix_steps': ['configure terminal', 'interface GigabitEthernet0/0.30', 'no shutdown']
        }

    if issue['issue'] == 'vlan_down':
        return {
            'root_cause': 'VLAN interface is down or missing',
            'osi_layer': 'Layer 2',
            'confidence': 0.88,
            'evidence': [issue['match_text'] or 'VLAN is reported as down'],
            'next_command': 'show vlan brief',
            'fix_steps': ['configure terminal', 'interface vlan 30', 'no shutdown']
        }

    if issue['issue'] == 'trunk_mismatch':
        return {
            'root_cause': 'Trunk or VLAN configuration is inconsistent with the valid topology',
            'osi_layer': 'Layer 2',
            'confidence': 0.87,
            'evidence': [issue['match_text'] or 'Switchport mode and encapsulation mismatch'],
            'next_command': 'show interfaces trunk',
            'fix_steps': ['configure terminal', 'interface GigabitEthernet0/1', 'switchport mode trunk', 'switchport trunk allowed vlan 10,20,30']
        }

    if issue['issue'] == 'access_list_block':
        return {
            'root_cause': 'Access control list is blocking the required service',
            'osi_layer': 'Layer 4',
            'confidence': 0.82,
            'evidence': [issue['match_text'] or 'ACL entries deny the target protocol'],
            'next_command': 'show access-lists',
            'fix_steps': ['configure terminal', 'ip access-list extended 101', 'permit tcp any any eq 22']
        }

    if issue['issue'] == 'dhcp_issue':
        return {
            'root_cause': 'DHCP service or addressing path is failing',
            'osi_layer': 'Layer 3',
            'confidence': 0.78,
            'evidence': [issue['match_text'] or '169.254.x.x indicates a failed DHCP acquisition'],
            'next_command': 'show ip dhcp binding',
            'fix_steps': ['configure terminal', 'service dhcp', 'ip dhcp pool LAN', 'network 10.0.30.0 255.255.255.0']
        }

    return {
        'root_cause': 'Potential configuration issue detected',
        'osi_layer': 'Layer 3',
        'confidence': 0.65,
        'evidence': [issue['match_text'] or 'No deterministic pattern was available'],
        'next_command': 'show running-config',
        'fix_steps': ['Validate the interface and routing configuration before remediation.']
    }
