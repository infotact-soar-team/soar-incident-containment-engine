from app.database.session import SessionLocal
from app.models.incident import Incident
from app.models.action import Action


def create_incident(alert_id: str, ioc_id: str, playbook_name: str) -> str:
    db = SessionLocal()
    try:
        incident = Incident(
            alert_id=alert_id,
            ioc_id=ioc_id,
            playbook_name=playbook_name,
            status="in_progress",
        )
        db.add(incident)
        db.commit()
        db.refresh(incident)
        return str(incident.id)
    finally:
        db.close()


def log_actions(incident_id: str, action_results: list) -> None:
    db = SessionLocal()
    try:
        for result in action_results:
            action = Action(
                incident_id=incident_id,
                action_type=result.get("action", "UNKNOWN"),
                target=result.get("target") or result.get("ip") or result.get("hostname"),
                success=result.get("success", False),
                details=str(result),
            )
            db.add(action)
        db.commit()

        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if incident:
            all_success = all(r.get("success", False) for r in action_results)
            incident.status = "contained" if all_success else "in_progress"
            db.commit()
    finally:
        db.close()