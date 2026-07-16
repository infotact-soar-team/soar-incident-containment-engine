from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_webhook_full_flow_creates_alert_and_iocs():
    payload = {
        "source": "Splunk",
        "severity": "critical",
        "message": "Suspicious connection from 185.220.101.1 to malicious-domain-example.com, dropped file 44d88612fea8a8f36de82e1278abb02f",
        "timestamp": "2026-07-16T10:00:00",
    }

    response = client.post("/webhook/alert", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "received"
    assert data["normalized_severity"] == "high"

    extracted_types = [ioc["type"] for ioc in data["extracted_iocs"]]
    assert "ip" in extracted_types
    assert "domain" in extracted_types
    assert "hash" in extracted_types


def test_webhook_handles_missing_fields_gracefully():
    payload = {"source": "UnknownTool"}

    response = client.post("/webhook/alert", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["normalized_severity"] == "low"
    assert data["extracted_iocs"] == []


def test_webhook_handles_clean_alert_with_no_iocs():
    payload = {
        "source": "Wazuh",
        "severity": "info",
        "message": "System rebooted normally",
        "timestamp": "2026-07-16T09:00:00",
    }

    response = client.post("/webhook/alert", json=payload)

    assert response.status_code == 200
    assert response.json()["extracted_iocs"] == []