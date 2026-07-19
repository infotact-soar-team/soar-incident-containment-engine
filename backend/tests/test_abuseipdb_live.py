import pytest
from unittest.mock import patch, MagicMock
from app.integrations.abuseipdb import check_ip


def test_check_ip_missing_api_key(monkeypatch):
    monkeypatch.setattr("app.integrations.abuseipdb.settings.ABUSEIPDB_API_KEY", "")
    with pytest.raises(ValueError):
        check_ip("185.220.101.1")


@patch("app.integrations.abuseipdb.httpx.get")
def test_check_ip_success(mock_get, monkeypatch):
    monkeypatch.setattr("app.integrations.abuseipdb.settings.ABUSEIPDB_API_KEY", "fake-key")

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "ipAddress": "185.220.101.1",
            "abuseConfidenceScore": 92,
            "countryCode": "DE",
            "totalReports": 145,
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = check_ip("185.220.101.1")
    assert result["abuse_confidence_score"] == 92
    assert result["country_code"] == "DE"