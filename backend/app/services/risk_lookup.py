"""
Internal service exposing risk score lookups for a given IoC,
so the playbook engine (Week 3) doesn't need to know about
Celery tasks or which TI integration was used — it just asks
"what's the current risk score for this IoC?"
"""
from app.database.session import SessionLocal
from app.models.ioc import IOC


def get_ioc_risk(ioc_id: str) -> dict:
    """
    Returns the persisted risk_score/severity/recommended_action
    for a given IoC (populated earlier by enrich_ioc_task).
    """
    db = SessionLocal()
    try:
        ioc = db.query(IOC).filter(IOC.id == ioc_id).first()
        if not ioc:
            return {"found": False}

        return {
            "found": True,
            "ioc_id": str(ioc.id),
            "ioc_type": ioc.ioc_type,
            "value": ioc.value,
            "risk_score": ioc.risk_score,
            "severity": ioc.severity,
            "recommended_action": ioc.recommended_action,
        }
    finally:
        db.close()


def get_risk_for_alert(alert_id: str) -> list:
    """
    Returns risk data for every IoC belonging to a given alert —
    useful when a playbook needs to evaluate the whole alert at once.
    """
    db = SessionLocal()
    try:
        iocs = db.query(IOC).filter(IOC.alert_id == alert_id).all()
        return [
            {
                "ioc_id": str(ioc.id),
                "ioc_type": ioc.ioc_type,
                "value": ioc.value,
                "risk_score": ioc.risk_score,
                "severity": ioc.severity,
                "recommended_action": ioc.recommended_action,
            }
            for ioc in iocs
        ]
    finally:
        db.close()