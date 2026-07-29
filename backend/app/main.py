from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pathlib import Path
import time
from app.core.logging_config import logger
from app.core.redis_client import check_redis_connection
from app.core.exceptions import global_exception_handler

# ✅ Create FastAPI app FIRST
app = FastAPI(
    title="SOAR Incident Containment Engine",
    version="0.1.0",
    description="Enterprise SOAR platform — webhook ingestion, enrichment, and automated containment"
)

# ✅ Import routers AFTER app creation
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.webhook import router as webhook_router
from app.api.incidents import router as incidents_router
from app.api.iocs import router as iocs_router
from app.api.playbook_control import router as playbook_control_router

# ✅ Register routers
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(webhook_router)
app.include_router(incidents_router)
app.include_router(iocs_router)
app.include_router(playbook_control_router)

# ✅ Exception handler
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


@app.get("/dashboard", include_in_schema=False)
def dashboard():
    return FileResponse(Path(__file__).parent / "static" / "dashboard.html")

# ✅ Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)")
    return response
