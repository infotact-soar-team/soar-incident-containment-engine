"""
Internal service exposing risk score lookups for a given IoC, now cached
so repeated lookups within a single playbook run (or re-run) don't
re-query the DB unnecessarily.
"""
from app.database.session import SessionLocal
from app.models.ioc import IOC
from app.services.cache import get_or_fetch


def _fetch_ioc_risk(ioc_id: str) -> dict:
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


def get_ioc_risk(ioc_id: str, use_cache: bool = True) -> dict:
    if not use_cache:
        return _fetch_ioc_risk(ioc_id)

    cache_key = f"risk_lookup:ioc:{ioc_id}"
    return get_or_fetch(cache_key, lambda: _fetch_ioc_risk(ioc_id), ttl=300)


def invalidate_ioc_risk_cache(ioc_id: str) -> None:
    """Call this whenever an IoC's risk_score is updated, so stale cache isn't served."""
    from app.core.redis_client import redis_client
    redis_client.delete(f"risk_lookup:ioc:{ioc_id}")


def get_risk_for_alert(alert_id: str) -> list:
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