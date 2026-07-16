from app.integrations.mock_edr import isolate_host, release_host, is_isolated


def test_isolate_host():
    result = isolate_host("WORKSTATION-07")
    assert result["success"] is True
    assert is_isolated("WORKSTATION-07") is True


def test_release_host():
    isolate_host("SERVER-02")
    release_host("SERVER-02")
    assert is_isolated("SERVER-02") is False

