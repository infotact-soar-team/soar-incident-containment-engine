from unittest.mock import patch
from app.database.session import SessionLocal
from app.models.alert import Alert
from app.models.ioc import IOC
from app.tasks.enrichment_task import enrich_ioc_task


@patch("app.tasks.enrichment_task.check_ip")
@patch("app.tasks.enrichment_task.lookup_ip_location")
def test_enrichment_task_writes_result_to_ioc_row(mock_geoip, mock_abuseipdb):
    mock_abuseipdb.return_value = {"abuse_confidence_score": 90}
    mock_geoip.return_value = {"country": "Germany"}

    db = SessionLocal()
    alert = Alert(source="Splunk", raw_payload="{}", severity="high", status="new")
    db.add(alert)
    db.commit()
    db.refresh(alert)

    ioc = IOC(alert_id=alert.id, ioc_type="ip", value="185.220.101.1")
    db.add(ioc)
    db.commit()
    db.refresh(ioc)
    ioc_id = str(ioc.id)
    db.close()

    enrich_ioc_task.run(ioc_id, "ip", "185.220.101.1")

    db2 = SessionLocal()
    updated_ioc = db2.query(IOC).filter(IOC.id == ioc_id).first()
    assert updated_ioc.risk_score == 90
    assert updated_ioc.severity == "high"
    db2.close()