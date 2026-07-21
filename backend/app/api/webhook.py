import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.alert import Alert
from app.models.ioc import IOC
from app.services.normalizer import normalize_alert
from app.services.ioc_extractor import extract_iocs
from app.tasks.enrichment_task import enrich_ioc_task

router = APIRouter()


@router.post("/webhook/alert")
def receive_alert(payload: dict, db: Session = Depends(get_db)):
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

    extracted = extract_iocs(normalized.message)
    saved_iocs = []
    for ioc_type, values in extracted.items():
        for value in values:
            ioc = IOC(alert_id=alert.id, ioc_type=ioc_type, value=value)
            db.add(ioc)
            db.commit()
            db.refresh(ioc)

            enrich_ioc_task.delay(str(ioc.id), ioc_type, value)
            saved_iocs.append({"type": ioc_type, "value": value, "ioc_id": str(ioc.id)})

    return {
        "alert_id": str(alert.id),
        "status": "received",
        "normalized_severity": normalized.severity,
        "extracted_iocs": saved_iocs,
    }