import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.alert import Alert
from app.services.normalizer import normalize_alert

router = APIRouter()


@router.post("/webhook/alert")
def receive_alert(payload: dict, db: Session = Depends(get_db)):
    """
    Ingestion endpoint. Stores the raw payload AND runs it through
    the normalizer immediately.
    """
    normalized = normalize_alert(payload)

    alert = Alert(
        source=normalized.source,
        raw_payload=json.dumps(payload),
        severity=normalized.severity,
        status="new",
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    return {
        "alert_id": str(alert.id),
        "status": "received",
        "normalized_severity": normalized.severity,
        "normalized_message": normalized.message,
    }