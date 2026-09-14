from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)


@app.get("/")
def root():
    return {
        "service": "payments-api",
        "status": "healthy"
    }


@app.get("/health")
def health():
    return {"status": "ok"}