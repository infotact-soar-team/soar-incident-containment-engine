from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_integrations_health_returns_all_sections():
    response = client.get("/health/integrations")
    assert response.status_code == 200
    data = response.json()

    assert "abuseipdb" in data
    assert "virustotal" in data
    assert "geoip" in data
    assert "redis" in data
    assert "api_key_configured" in data["abuseipdb"]