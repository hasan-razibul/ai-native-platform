import httpx
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from models.intent import CreateServiceIntent
from services.llm.ollama_provider import OllamaProvider

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


def test_interpret_service_request():
    mock_intent = {
        "action": "create_service",
        "service": {
            "name": "payments-api",
            "language": "python",
            "port": 8000,
            "replicas": 3,
        },
        "environment": "staging",
    }

    with patch.object(
            OllamaProvider,
            "interpret_service_request",
    ) as mock_interpret:
        mock_interpret.return_value = CreateServiceIntent.model_validate(
            mock_intent
        )

        response = client.post(
            "/api/v1/intents/interpret",
            json={
                "request": (
                    "Create a Python service named payments-api "
                    "in staging using port 8000 and 3 replicas."
                )
            },
        )

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
    assert response.json()["intent"] == mock_intent
    mock_interpret.assert_called_once()


def test_interpret_returns_503_when_ollama_is_unavailable():
    with patch.object(
            OllamaProvider,
            "interpret_service_request",
            side_effect=httpx.ConnectError("Connection refused"),
    ):
        response = client.post(
            "/api/v1/intents/interpret",
            json={"request": "Create a Python payments service."},
        )

    assert response.status_code == 503
    assert "Ollama is unavailable" in response.json()["detail"]


def test_interpret_rejects_short_request():
    response = client.post(
        "/api/v1/intents/interpret",
        json={"request": "Create"},
    )

    assert response.status_code == 422