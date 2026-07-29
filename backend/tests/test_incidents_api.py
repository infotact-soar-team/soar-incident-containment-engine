from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal
from app.models.alert import Alert
from app.models.incident import Incident
from app.models.action import Action
from app.auth.jwt_handler import create_access_token

client = TestClient(app)
AUTH_HEADERS = {"Authorization": f"Bearer {create_access_token('admin_user', 'admin')}"}


def test_list_incidents_empty_ok():
    response = client.get("/incidents", headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert "total" in response.json()


def test_list_and_get_actions_for_incident():
    db = SessionLocal()
    alert = Alert(source="Splunk", raw_payload="{}", severity="high", status="contained")
    db.add(alert)
    db.commit()
    db.refresh(alert)

    incident = Incident(alert_id=alert.id, playbook_name="malicious_ip_playbook", status="contained")
    db.add(incident)
    db.commit()
    db.refresh(incident)

    action = Action(incident_id=incident.id, action_type="BLOCK_IP", target="1.2.3.4", success=True)
    db.add(action)
    db.commit()
    incident_id = str(incident.id)
    db.close()

    list_response = client.get("/incidents", headers=AUTH_HEADERS)
    assert list_response.status_code == 200
    assert list_response.json()["total"] >= 1

    actions_response = client.get(f"/incidents/{incident_id}/actions", headers=AUTH_HEADERS)
    assert actions_response.status_code == 200
    assert len(actions_response.json()) == 1


def test_get_actions_for_nonexistent_incident():
    response = client.get(
        "/incidents/00000000-0000-0000-0000-000000000000/actions",
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 404
