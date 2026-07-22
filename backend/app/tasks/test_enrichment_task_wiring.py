from unittest.mock import patch
from app.tasks.enrichment_task import enrich_ioc_task


@patch("app.tasks.enrichment_task.check_ip")
@patch("app.tasks.enrichment_task.lookup_ip_location")
def test_enrichment_task_full_flow_for_ip(mock_geoip, mock_abuseipdb):
    mock_abuseipdb.return_value = {"abuse_confidence_score": 95}
    mock_geoip.return_value = {"country": "Germany"}

    result = enrich_ioc_task.run("fake-ioc-id", "ip", "185.220.101.1")

    assert result["status"] == "enriched"
    assert result["risk_score"] == 95
    assert result["severity"] == "high"
    assert result["recommended_action"] == "AUTO_CONTAIN"


@patch("app.tasks.enrichment_task.check_hash")
def test_enrichment_task_full_flow_for_hash(mock_vt):
    mock_vt.return_value = {"malicious": 2, "suspicious": 0, "harmless": 8, "undetected": 0}

    result = enrich_ioc_task.run("fake-ioc-id", "hash", "44d88612fea8a8f36de82e1278abb02f")

    assert result["status"] == "enriched"
    assert result["severity"] == "low"


def test_enrichment_task_unknown_ioc_type():
    result = enrich_ioc_task.run("fake-ioc-id", "url", "http://example.com")
    assert result["status"] == "skipped"
    