import os
from fastapi import APIRouter
from app.core.config import settings
from app.core.redis_client import check_redis_connection

router = APIRouter()


@router.get("/health/integrations")
def integrations_health():
    return {
        "abuseipdb": {
            "api_key_configured": bool(settings.ABUSEIPDB_API_KEY),
        },
        "virustotal": {
            "api_key_configured": bool(settings.VIRUSTOTAL_API_KEY),
        },
        "geoip": {
            "database_file_found": os.path.isfile(settings.GEOLITE2_DB_PATH),
            "expected_path": settings.GEOLITE2_DB_PATH,
        },
        "redis": {
            "connected": check_redis_connection(),
        },
    }