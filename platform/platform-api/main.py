from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx

from models.intent import CreateServiceIntent
from services.llm.ollama_provider import OllamaProvider

app = FastAPI(
    title="AI-Native Platform API",
    description="API for requesting and validating application services.",
    version="0.2.0",
)

ollama_provider = OllamaProvider()


class InterpretRequest(BaseModel):
    request: str = Field(min_length=10, max_length=2000)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/api/v1/intents/services")
def create_service_intent(intent: CreateServiceIntent) -> dict:
    return {
        "status": "accepted",
        "message": "Service intent validated successfully.",
        "intent": intent.model_dump(),
    }


@app.post("/api/v1/intents/interpret")
def interpret_service_request(body: InterpretRequest) -> dict:
    try:
        intent = ollama_provider.interpret_service_request(body.request)
    except httpx.ConnectError as exc:
        raise HTTPException(
            status_code=503,
            detail="Ollama is unavailable. Ensure Ollama is running.",
        ) from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=504,
            detail="Ollama did not respond in time.",
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="Ollama returned an unsuccessful response.",
        ) from exc
    except (ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Ollama returned an invalid service intent.",
        ) from exc

    return {
        "status": "accepted",
        "message": "Service intent interpreted and validated successfully.",
        "intent": intent.model_dump(),
    }
