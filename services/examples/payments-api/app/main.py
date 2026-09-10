from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "service": "payments-api",
        "status": "healthy"
    }


@app.get("/health")
def health():
    return {"status": "ok"}