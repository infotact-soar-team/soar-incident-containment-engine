"""
Manages the Alert lifecycle state machine.
Valid transitions: new -> enriched -> triaged -> contained
"""
from app.database.session import SessionLocal
from app.models.alert import Alert

VALID_TRANSITIONS = {
    "new": ["enriched"],
    "enriched": ["triaged"],
    "triaged": ["contained"],
    "contained": [],  # terminal state
}


class InvalidTransitionError(Exception):
    pass


def transition_alert(alert_id: str, new_status: str) -> dict:
    db = SessionLocal()
    try:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return {"found": False}

        current = alert.status
        allowed = VALID_TRANSITIONS.get(current, [])

        if new_status not in allowed:
            raise InvalidTransitionError(
                f"Cannot transition from '{current}' to '{new_status}'. Allowed: {allowed}"
            )

        alert.status = new_status
        db.commit()

        return {"found": True, "alert_id": str(alert.id), "old_status": current, "new_status": new_status}
    finally:
        db.close()