from app.database.session import SessionLocal
from app.models.alert import Alert
from app.models.ioc import IOC
from app.models.incident import Incident
from app.models.action import Action
from app.services.incident_service import create_incident, log_actions


def test_create_incident_and_log_actions():
    db = SessionLocal()
    alert = Alert(source="Splunk", raw_payload="{}", severity="high", status="enriched")
    db.add(alert)
    db.commit()
    db.refresh(alert)

    ioc = IOC(alert_id=alert.id, ioc_type="ip", value="185.220.101.1", risk_score=95, severity="high")
    db.add(ioc)
    db.commit()
    db.refresh(ioc)
    alert_id, ioc_id = str(alert.id), str(ioc.id)
    db.close()

    incident_id = create_incident(alert_id, ioc_id, "malicious_ip_playbook")

    log_actions(incident_id, [
        {"action": "BLOCK_IP", "ip": "185.220.101.1", "success": True},
        {"action": "NOTIFY_ANALYST", "target": "185.220.101.1", "success": True},
    ])

    db2 = SessionLocal()
    incident = db2.query(Incident).filter(Incident.id == incident_id).first()
    actions = db2.query(Action).filter(Action.incident_id == incident_id).all()

    assert incident.status == "contained"
    assert len(actions) == 2
    db2.close()