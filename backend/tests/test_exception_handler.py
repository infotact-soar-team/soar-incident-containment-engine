from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.core.exceptions import global_exception_handler

test_app = FastAPI()
test_app.add_exception_handler(Exception, global_exception_handler)


@test_app.get("/boom")
def boom():
    raise ValueError("Something broke")


client = TestClient(test_app, raise_server_exceptions=False)


def test_global_exception_handler_returns_500_json():
    response = client.get("/boom")
    assert response.status_code == 500
    assert response.json()["error"] == "Internal server error"