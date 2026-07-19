from app.integrations.mock_firewall import block_ip, is_blocked
from app.integrations.mock_edr import isolate_host, is_isolated
from app.integrations.aws_sg import isolate_via_security_group


def test_full_containment_simulation_for_high_risk_alert():
    """
    Simulates what a high-risk playbook execution will do in Week 3:
    block the IP, isolate the affected host, AND isolate via AWS SG,
    all logged and successful.
    """
    malicious_ip = "185.220.101.1"
    affected_host = "WORKSTATION-07"

    firewall_result = block_ip(malicious_ip)
    edr_result = isolate_host(affected_host)
    aws_result = isolate_via_security_group(malicious_ip)

    assert firewall_result["success"] is True
    assert edr_result["success"] is True
    assert aws_result["success"] is True

    assert is_blocked(malicious_ip) is True
    assert is_isolated(affected_host) is True


def test_containment_actions_are_independent():
    """Blocking one IP should not affect isolation state of another host."""
    block_ip("1.1.1.1")
    assert is_isolated("SOME-OTHER-HOST") is False
