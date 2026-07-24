from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal
from app.models.alert import Alert
from app.models.ioc import IOC

client = TestClient(app)


@patch("app.api.webhook.enrich_ioc_task.delay")
def test_full_pipeline_webhook_to_enrichment_dispatch(mock_delay):
    """
    End-to-end: post a raw alert -> gets normalized -> IoCs extracted
    and saved to DB -> enrichment task dispatched per IoC.
    """
    payload = {
        "source": "Splunk",
        "severity": "critical",
        "message": "Suspicious connection from 185.220.101.1 to malicious-domain-example.com, dropped file 44d88612fea8a8f36de82e1278abb02f",
        "timestamp": "2026-07-20T10:00:00",
    }

    response = client.post("/webhook/alert", json=payload)
    assert response.status_code == 200
    data = response.json()

    # 1. Alert was created with normalized severity
    assert data["normalized_severity"] == "high"

    # 2. All 3 IoC types were extracted
    extracted_types = {ioc["type"] for ioc in data["extracted_iocs"]}
    assert extracted_types == {"ip", "domain", "hash"}

    # 3. An enrichment task was dispatched per IoC
    assert mock_delay.call_count == 3

    # 4. Alert and IoCs actually persisted in the DB
    db = SessionLocal()
    try:
        alert = db.query(Alert).filter(Alert.id == data["alert_id"]).first()
        assert alert is not None
        assert alert.severity == "high"

        iocs = db.query(IOC).filter(IOC.alert_id == alert.id).all()
        assert len(iocs) == 3
    finally:
        db.close()


@patch("app.api.webhook.enrich_ioc_task.delay")
def test_full_pipeline_no_iocs_still_succeeds(mock_delay):
    payload = {"source": "Wazuh", "severity": "info", "message": "System rebooted normally"}
    response = client.post("/webhook/alert", json=payload)

    assert response.status_code == 200
    assert response.json()["extracted_iocs"] == []
    assert mock_delay.call_count == 0