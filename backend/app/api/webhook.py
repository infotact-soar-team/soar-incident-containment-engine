import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.alert import Alert

router = APIRouter()


@router.post("/webhook/alert")
def receive_alert(payload: dict, db: Session = Depends(get_db)):
    """
    Raw ingestion endpoint. Accepts any JSON alert payload from a SIEM,
    stores it as-is (normalization happens in a later step).
    """
    alert = Alert(
        source=payload.get("source", "unknown"),
        raw_payload=json.dumps(payload),
        severity="unknown",
        status="new",
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    return {"alert_id": str(alert.id), "status": "received"}