"""
AbuseIPDB Integration — live, cached, with retry/backoff.
"""
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.config import settings
from app.services.cache import get_or_fetch

ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError)),
)
def _fetch_ip(ip: str) -> dict:
    if not settings.ABUSEIPDB_API_KEY:
        raise ValueError("ABUSEIPDB_API_KEY is not set in environment/.env")

    headers = {"Key": settings.ABUSEIPDB_API_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}

    response = httpx.get(ABUSEIPDB_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()["data"]

    return {
        "ip": data.get("ipAddress"),
        "abuse_confidence_score": data.get("abuseConfidenceScore"),
        "country_code": data.get("countryCode"),
        "total_reports": data.get("totalReports"),
    }


def check_ip(ip: str) -> dict:
    cache_key = f"abuseipdb:ip:{ip}"
    return get_or_fetch(cache_key, lambda: _fetch_ip(ip), ttl=3600)
