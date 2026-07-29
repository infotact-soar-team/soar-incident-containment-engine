from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.auth.jwt_handler import create_access_token

client = TestClient(app)


@patch("app.tasks.enrichment_task.check_ip")
@patch("app.tasks.enrichment_task.lookup_ip_location")
def test_end_to_end_alert_to_incident_visible_in_api(mock_geoip, mock_abuseipdb):
    """
    Full sanity check: webhook -> normalize -> extract -> enrich (sync via .run) ->
    playbook -> incident created -> visible via /incidents API.
    """
    mock_abuseipdb.return_value = {"abuse_confidence_score": 96}
    mock_geoip.return_value = {"country": "Russia"}

    payload = {
        "source": "Splunk",
        "severity": "critical",
        "message": "Suspicious connection from 185.220.101.1 detected",
    }
    response = client.post("/webhook/alert", json=payload)
    assert response.status_code == 200
    ioc_id = response.json()["extracted_iocs"][0]["ioc_id"]

    from app.tasks.enrichment_task import enrich_ioc_task
    result = enrich_ioc_task.run(ioc_id, "ip", "185.220.101.1")
    assert result["incident_id"] is not None

    token = create_access_token("admin", "admin")
    incidents_response = client.get("/incidents", headers={"Authorization": f"Bearer {token}"})
    assert incidents_response.status_code == 200
    assert incidents_response.json()["total"] >= 1