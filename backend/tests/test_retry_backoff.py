import httpx
from unittest.mock import patch, MagicMock
from app.integrations.abuseipdb import _fetch_ip


@patch("app.integrations.abuseipdb.httpx.get")
def test_fetch_ip_retries_on_timeout_then_succeeds(mock_get, monkeypatch):
    monkeypatch.setattr("app.integrations.abuseipdb.settings.ABUSEIPDB_API_KEY", "fake-key")

    success_response = MagicMock()
    success_response.json.return_value = {
        "data": {"ipAddress": "1.2.3.4", "abuseConfidenceScore": 50, "countryCode": "US", "totalReports": 3}
    }
    success_response.raise_for_status.return_value = None

    mock_get.side_effect = [httpx.TimeoutException("timed out"), success_response]

    result = _fetch_ip("1.2.3.4")
    assert result["abuse_confidence_score"] == 50
    assert mock_get.call_count == 2  # failed once, succeeded on retry


@patch("app.integrations.abuseipdb.httpx.get")
def test_fetch_ip_gives_up_after_max_attempts(mock_get, monkeypatch):
    monkeypatch.setattr("app.integrations.abuseipdb.settings.ABUSEIPDB_API_KEY", "fake-key")
    mock_get.side_effect = httpx.TimeoutException("always times out")

    try:
        _fetch_ip("1.2.3.4")
        assert False, "Expected an exception after retries exhausted"
    except Exception:
        pass

    assert mock_get.call_count == 3  # stop_after_attempt(3)