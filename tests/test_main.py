from fastapi.testclient import TestClient
from app.main import app

def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "application": "MarketPulse",
        "status": "running",
    }


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }