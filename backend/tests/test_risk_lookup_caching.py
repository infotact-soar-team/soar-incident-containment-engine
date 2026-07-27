from unittest.mock import patch
from app.database.session import SessionLocal
from app.models.alert import Alert
from app.models.ioc import IOC
from app.services.risk_lookup import get_ioc_risk, invalidate_ioc_risk_cache


def _create_ioc_with_risk(risk_score=80):
    db = SessionLocal()
    alert = Alert(source="Splunk", raw_payload="{}", severity="high", status="new")
    db.add(alert)
    db.commit()
    db.refresh(alert)

    ioc = IOC(alert_id=alert.id, ioc_type="ip", value="1.2.3.4", risk_score=risk_score)
    db.add(ioc)
    db.commit()
    db.refresh(ioc)
    ioc_id = str(ioc.id)
    db.close()
    return ioc_id


def test_repeated_lookup_hits_cache():
    ioc_id = _create_ioc_with_risk(80)

    with patch("app.services.risk_lookup._fetch_ioc_risk", wraps=lambda x: {"found": True, "risk_score": 80}) as mock_fetch:
        get_ioc_risk(ioc_id)
        get_ioc_risk(ioc_id)
        assert mock_fetch.call_count == 1


def test_invalidate_cache_forces_refetch():
    ioc_id = _create_ioc_with_risk(50)
    get_ioc_risk(ioc_id)
    invalidate_ioc_risk_cache(ioc_id)

    with patch("app.services.risk_lookup._fetch_ioc_risk", wraps=lambda x: {"found": True, "risk_score": 50}) as mock_fetch:
        get_ioc_risk(ioc_id)
        assert mock_fetch.call_count == 1