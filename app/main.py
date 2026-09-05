from fastapi import FastAPI

app = FastAPI(
    title="MarketPulse",
    description="Real-Time Market Intelligence & Analytics Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "application": "MarketPulse",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }