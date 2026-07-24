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


def test_enrichment_task_runs_synchronously():
    from app.tasks.enrichment_task import enrich_ioc_task
    result = enrich_ioc_task.run("fake-id", "ip", "1.2.3.4")
    assert result["status"] == "dispatched"