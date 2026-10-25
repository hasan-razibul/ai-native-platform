from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_returns_service_information():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "service": "payments-api",
        "status": "healthy",
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "http_requests_total" in response.text