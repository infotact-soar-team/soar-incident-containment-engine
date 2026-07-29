from unittest.mock import patch
from app.services.cache import get_or_fetch
from app.integrations.abuseipdb import check_ip


@patch("app.integrations.abuseipdb.httpx.get")
def test_enrichment_cache_survives_repeated_alerts_for_same_ip(mock_get, monkeypatch):
    """
    Sanity check: if the same malicious IP appears in multiple alerts,
    the second+ enrichment should hit cache, not the live API.
    """
    from unittest.mock import MagicMock
    monkeypatch.setattr("app.integrations.abuseipdb.settings.ABUSEIPDB_API_KEY", "fake-key")

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {"ipAddress": "1.2.3.4", "abuseConfidenceScore": 88, "countryCode": "US", "totalReports": 5}
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result1 = check_ip("1.2.3.4")
    result2 = check_ip("1.2.3.4")
    result3 = check_ip("1.2.3.4")

    assert result1 == result2 == result3
    assert mock_get.call_count == 1


def test_enrichment_result_schema_is_json_serializable():
    """Ensures enrichment results won't break API serialization on the dashboard side."""
    import json
    from app.schemas.enrichment import EnrichmentResult

    result = EnrichmentResult(ioc_value="1.2.3.4", ioc_type="ip", risk_score=90)
    json.dumps(result.model_dump())  # should not raise