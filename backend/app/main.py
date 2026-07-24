from fastapi import FastAPI, Request
import time

from app.api.webhook import router as webhook_router
from app.core.exceptions import global_exception_handler
from app.core.logging_config import logger
from app.core.redis_client import check_redis_connection

# ✅ Create FastAPI app FIRST
app = FastAPI(
    title="SOAR Incident Containment Engine",
    version="0.1.0",
    description="Enterprise SOAR platform — webhook ingestion, enrichment, and automated containment"
)

# ✅ Register routers and handlers AFTER app creation
app.include_router(webhook_router)
app.add_exception_handler(Exception, global_exception_handler)

# ✅ Health endpoints
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "soar-incident-engine"}

@app.get("/health/redis")
def redis_health():
    is_up = check_redis_connection()
    return {"redis_connected": is_up}

@app.get("/")
def root():
    return {"message": "SOAR Incident Containment Engine API is running"}

# ✅ Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)")
    return response
