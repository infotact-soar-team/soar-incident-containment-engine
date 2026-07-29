from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.api.webhook.enrich_ioc_task.delay")
def test_webhook_dispatches_enrichment_task_per_ioc(mock_delay):
    payload = {
        "source": "Splunk",
        "severity": "critical",
        "message": "Connection from 185.220.101.1 to evil-domain-example.com",
    }
    response = client.post("/webhook/alert", json=payload)

    assert response.status_code == 200
    assert mock_delay.call_count == 2  # one for the ip, one for the domain


@patch("app.tasks.enrichment_task.check_ip")
@patch("app.tasks.enrichment_task.lookup_ip_location")
def test_enrichment_task_runs_synchronously(mock_geoip, mock_abuseipdb):
    from app.tasks.enrichment_task import enrich_ioc_task

    mock_abuseipdb.return_value = {"abuse_confidence_score": 10}
    mock_geoip.return_value = {"country": "US"}

    result = enrich_ioc_task.run("fake-id", "ip", "1.2.3.4")
    assert result["status"] == "enriched"
    assert result["risk_score"] == 10
