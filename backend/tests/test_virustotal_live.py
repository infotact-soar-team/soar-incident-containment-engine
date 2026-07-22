import pytest
from unittest.mock import patch, MagicMock
from app.integrations.virustotal import check_hash, check_domain

def test_check_hash_missing_api_key(monkeypatch):
    monkeypatch.setattr("app.integrations.virustotal.settings.VIRUSTOTAL_API_KEY", "")
    with pytest.raises(ValueError):
        check_hash("44d88612fea8a8f36de82e1278abb02f")


@patch("app.integrations.virustotal.httpx.get")
def test_check_hash_success(mock_get, monkeypatch):
    monkeypatch.setattr("app.integrations.virustotal.settings.VIRUSTOTAL_API_KEY", "fake-key")

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "attributes": {
                "last_analysis_stats": {
                    "malicious": 58, "suspicious": 2, "harmless": 0, "undetected": 12
                }
            }
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = check_hash("44d88612fea8a8f36de82e1278abb02f")
    assert result["malicious"] == 58


@patch("app.integrations.virustotal.httpx.get")
def test_check_domain_success(mock_get, monkeypatch):
    monkeypatch.setattr("app.integrations.virustotal.settings.VIRUSTOTAL_API_KEY", "fake-key")

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "attributes": {
                "last_analysis_stats": {
                    "malicious": 15, "suspicious": 3, "harmless": 5, "undetected": 60
                }
            }
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = check_domain("malicious-domain-example.com")
    assert result["malicious"] == 15


    from app.core.rate_limiter import check_rate_limit


def check_hash(file_hash: str) -> dict:
    check_rate_limit("virustotal", max_requests=4, window_seconds=60)
    url = f"{VT_BASE_URL}/files/{file_hash}"
    response = httpx.get(url, headers=_get_headers(), timeout=10)
    response.raise_for_status()
    data = response.json()["data"]
    stats = data["attributes"]["last_analysis_stats"]

    return {
        "hash": file_hash,
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
        "undetected": stats.get("undetected", 0),
    }


def check_domain(domain: str) -> dict:
    check_rate_limit("virustotal", max_requests=4, window_seconds=60)
    url = f"{VT_BASE_URL}/domains/{domain}"
    response = httpx.get(url, headers=_get_headers(), timeout=10)
    response.raise_for_status()
    data = response.json()["data"]
    stats = data["attributes"]["last_analysis_stats"]

    return {
        "domain": domain,
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
        "undetected": stats.get("undetected", 0),
    }