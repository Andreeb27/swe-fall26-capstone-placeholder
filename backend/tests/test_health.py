from fastapi.testclient import TestClient

from app.infrastructure.config import Settings
from app.main import create_app


def test_health_ok():
    client = TestClient(create_app(Settings(scale_driver="simulated")))
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "scale_driver": "simulated"}


def test_frontend_is_served():
    client = TestClient(create_app(Settings(scale_driver="simulated")))
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello World" in response.text
