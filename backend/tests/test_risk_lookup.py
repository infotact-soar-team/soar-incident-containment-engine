from app.database.session import SessionLocal
from app.models.alert import Alert
from app.models.ioc import IOC
from app.services.risk_lookup import get_ioc_risk, get_risk_for_alert


def test_get_ioc_risk_found():
    db = SessionLocal()
    alert = Alert(source="Splunk", raw_payload="{}", severity="high", status="new")
    db.add(alert)
    db.commit()
    db.refresh(alert)

    ioc = IOC(alert_id=alert.id, ioc_type="ip", value="185.220.101.1", risk_score=90, severity="high")
    db.add(ioc)
    db.commit()
    db.refresh(ioc)
    ioc_id = str(ioc.id)
    db.close()

    result = get_ioc_risk(ioc_id)
    assert result["found"] is True
    assert result["risk_score"] == 90


def test_get_ioc_risk_not_found():
    result = get_ioc_risk("00000000-0000-0000-0000-000000000000")
    assert result["found"] is False


def test_get_risk_for_alert_returns_all_iocs():
    db = SessionLocal()
    alert = Alert(source="Wazuh", raw_payload="{}", severity="medium", status="new")
    db.add(alert)
    db.commit()
    db.refresh(alert)

    ioc1 = IOC(alert_id=alert.id, ioc_type="ip", value="1.2.3.4", risk_score=40)
    ioc2 = IOC(alert_id=alert.id, ioc_type="domain", value="test.com", risk_score=60)
    db.add_all([ioc1, ioc2])
    db.commit()
    alert_id = str(alert.id)
    db.close()

    results = get_risk_for_alert(alert_id)
    assert len(results) == 2