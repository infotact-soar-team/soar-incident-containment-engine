from unittest.mock import patch
from app.database.session import SessionLocal
from app.models.alert import Alert
from app.models.ioc import IOC
from app.tasks.enrichment_task import enrich_ioc_task



@patch("app.tasks.enrichment_task.check_ip")
@patch("app.tasks.enrichment_task.lookup_ip_location")
def test_pipeline_still_works_after_db_index_changes(mock_geoip, mock_abuseipdb):
    """
    Regression check: confirms the enrichment pipeline still reads/writes
    correctly after Hardik's index migration and Praveen's caching/retry work.
    """
    # Mock upstream TI calls
    mock_abuseipdb.return_value = {"abuse_confidence_score": 88}
    mock_geoip.return_value = {"country": "Russia"}

    # Insert an alert
    db = SessionLocal()
    alert = Alert(source="Splunk", raw_payload="{}", severity="high", status="new")
    db.add(alert)
    db.commit()
    db.refresh(alert)

    # Insert an IOC linked to that alert
    ioc = IOC(alert_id=alert.id, ioc_type="ip", value="45.155.205.1")
    db.add(ioc)
    db.commit()
    db.refresh(ioc)
    ioc_id = str(ioc.id)
    db.close()

    # Run enrichment pipeline
    result = enrich_ioc_task.run(ioc_id, "ip", "45.155.205.1")

    # Assert enrichment results
    assert result["status"] == "enriched"
    assert result["risk_score"] == 88
    assert result["severity"] == "high"

    # Verify DB updated correctly
    db2 = SessionLocal()
    updated = db2.query(IOC).filter(IOC.id == ioc_id).first()
    assert updated.risk_score == 88
    assert updated.severity == "high"
    db2.close()


def test_alert_query_by_severity_uses_index_fast():
    """Sanity check: querying by severity (now indexed) still returns correct results."""
    db = SessionLocal()
    alert = Alert(source="Wazuh", raw_payload="{}", severity="medium", status="new")
    db.add(alert)
    db.commit()

    results = db.query(Alert).filter(Alert.severity == "medium").all()
    assert any(a.id == alert.id for a in results)
    db.close()
