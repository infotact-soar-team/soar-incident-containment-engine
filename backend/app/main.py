from fastapi import FastAPI
from app.api.webhook import router as webhook_router

app.include_router(webhook_router)

app = FastAPI(
    title="SOAR Incident Containment Engine",
    version="0.1.0",
    description="Enterprise SOAR platform - webhook ingestion, enrichment, and automated containment"
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "soar-incident-engine"}


@app.get("/")
def root():
    return {"message": "SOAR Incident Containment Engine API is running"}
from app.core.redis_client import check_redis_connection


@app.get("/health/redis")
def redis_health():
    is_up = check_redis_connection()
    return {"redis_connected": is_up}