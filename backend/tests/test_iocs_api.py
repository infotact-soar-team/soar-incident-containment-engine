from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal
from app.models.alert import Alert
from app.models.ioc import IOC
from app.auth.jwt_handler import create_access_token

client = TestClient(app)
AUTH_HEADERS = {"Authorization": f"Bearer {create_access_token('admin_user', 'admin')}"}


def test_get_ioc_enrichment():
    db = SessionLocal()
    alert = Alert(source="Splunk", raw_payload="{}", severity="high", status="enriched")
    db.add(alert)
    db.commit()
    db.refresh(alert)

    ioc = IOC(alert_id=alert.id, ioc_type="ip", value="185.220.101.1", risk_score=92, severity="high")
    db.add(ioc)
    db.commit()
    db.refresh(ioc)
    ioc_id = str(ioc.id)
    db.close()

    response = client.get(f"/iocs/{ioc_id}/enrichment", headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert response.json()["risk_score"] == 92


def test_get_ioc_enrichment_not_found():
    response = client.get(
        "/iocs/00000000-0000-0000-0000-000000000000/enrichment",
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 404


def test_search_iocs_by_value():
    response = client.get("/iocs/search?value=185.220", headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_iocs_by_min_risk():
    response = client.get("/iocs/search?min_risk=90", headers=AUTH_HEADERS)
    assert response.status_code == 200
