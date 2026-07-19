from app.integrations.aws_sg import isolate_via_security_group


def test_isolate_via_security_group():
    result = isolate_via_security_group("185.220.101.1")
    assert result["success"] is True
    assert result["ip"] == "185.220.101.1"
    assert "security_group_id" in result
