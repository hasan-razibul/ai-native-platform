from fastapi import FastAPI

from models.intent import CreateServiceIntent

app = FastAPI(
    title="AI-Native Platform API",
    description="API for requesting and validating application services.",
    version="0.1.0",
)


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