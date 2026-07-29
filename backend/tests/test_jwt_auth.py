from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_success():
    response = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["role"] == "admin"


def test_login_wrong_password():
    response = client.post("/auth/login", json={"username": "admin", "password": "wrongpass"})
    assert response.status_code == 401


def test_login_unknown_user():
    response = client.post("/auth/login", json={"username": "nobody", "password": "x"})
    assert response.status_code == 401


def test_token_decodes_correctly():
    from app.auth.jwt_handler import create_access_token, decode_access_token
    token = create_access_token("admin", "admin")
    payload = decode_access_token(token)
    assert payload["sub"] == "admin"
    assert payload["role"] == "admin"