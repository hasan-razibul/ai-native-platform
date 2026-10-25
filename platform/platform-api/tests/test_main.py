from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_service_intent():
    payload = {
        "action": "create_service",
        "service": {
            "name": "payments-api",
            "language": "python",
            "port": 8000,
            "replicas": 2,
        },
        "environment": "dev",
    }

    response = client.post("/api/v1/intents/services", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
    assert response.json()["intent"]["service"]["name"] == "payments-api"


def test_invalid_environment_is_rejected():
    payload = {
        "action": "create_service",
        "service": {
            "name": "payments-api",
            "language": "python",
            "port": 8000,
            "replicas": 2,
        },
        "environment": "testing",
    }

    response = client.post("/api/v1/intents/services", json=payload)

    assert response.status_code == 422


def test_invalid_replica_count_is_rejected():
    payload = {
        "action": "create_service",
        "service": {
            "name": "payments-api",
            "language": "python",
            "port": 8000,
            "replicas": 0,
        },
        "environment": "dev",
    }

    response = client.post("/api/v1/intents/services", json=payload)

    assert response.status_code == 422