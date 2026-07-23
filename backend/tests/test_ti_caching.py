from unittest.mock import patch, MagicMock
from app.integrations.abuseipdb import check_ip


@patch("app.integrations.abuseipdb.httpx.get")
def test_abuseipdb_result_is_cached(mock_get, monkeypatch):
    monkeypatch.setattr("app.integrations.abuseipdb.settings.ABUSEIPDB_API_KEY", "fake-key")

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {"ipAddress": "1.2.3.4", "abuseConfidenceScore": 80, "countryCode": "US", "totalReports": 10}
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result1 = check_ip("1.2.3.4")
    result2 = check_ip("1.2.3.4")

    assert result1 == result2
    assert mock_get.call_count == 1  # second call should hit cache, not the API