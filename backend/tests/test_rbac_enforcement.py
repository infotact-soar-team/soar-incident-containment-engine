from fastapi.testclient import TestClient
from app.main import app
from app.auth.jwt_handler import create_access_token

client = TestClient(app)


def test_incidents_requires_auth():
    response = client.get("/incidents")
    assert response.status_code == 401


def test_incidents_works_with_valid_token():
    token = create_access_token("viewer_user", "viewer")
    response = client.get("/incidents", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_dashboard_page_loads():
    response = client.get("/dashboard")
    assert response.status_code == 200