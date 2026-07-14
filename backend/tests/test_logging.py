from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_request_logging_does_not_break_response():
    response = client.get("/health")
    assert response.status_code == 200