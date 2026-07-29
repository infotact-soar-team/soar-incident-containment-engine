from fastapi.testclient import TestClient
from app.main import app
from app.auth.jwt import create_access_token
from app.database.session import SessionLocal
from app.models.alert import Alert
from app.models.ioc import IOC
from app.models.incident import Incident

client = TestClient(app)


def _setup_incident():
    db = SessionLocal()
    alert = Alert(source="Splunk", raw_payload="{}", severity="high", status="contained")
    db.add(alert)
    db.commit()
    db.refresh(alert)

    ioc = IOC(alert_id=alert.id, ioc_type="ip", value="185.220.101.1", risk_score=95, severity="high")
    db.add(ioc)
    db.commit()
    db.refresh(ioc)

    incident = Incident(alert_id=alert.id, ioc_id=ioc.id, playbook_name="malicious_ip_playbook", status="contained")
    db.add(incident)
    db.commit()
    db.refresh(incident)
    incident_id = str(incident.id)
    db.close()
    return incident_id


def test_rerun_requires_auth():
    incident_id = _setup_incident()
    response = client.post(f"/incidents/{incident_id}/rerun")
    assert response.status_code == 401


def test_rerun_as_analyst_succeeds():
    incident_id = _setup_incident()
    token = create_access_token("analyst_user", "analyst")
    response = client.post(f"/incidents/{incident_id}/rerun", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["actions_taken"] == 2


def test_rerun_as_viewer_forbidden():
    incident_id = _setup_incident()
    token = create_access_token("viewer_user", "viewer")
    response = client.post(f"/incidents/{incident_id}/rerun", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
