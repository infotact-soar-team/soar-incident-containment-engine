from app.integrations.mock_firewall import block_ip, unblock_ip, is_blocked

def test_block_ip():
    result = block_ip("185.220.101.1")
    assert result["success"] is True
    assert is_blocked("185.220.101.1") is True

def test_unblock_ip():
    block_ip("1.2.3.4")
    unblock_ip("1.2.3.4")
    assert is_blocked("1.2.3.4") is False
