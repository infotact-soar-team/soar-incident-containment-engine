"""
AbuseIPDB Integration — live implementation, now cached.
Docs: https://docs.abuseipdb.com/
Auth: API key via header 'Key'
Rate limit (free tier): 1,000 checks/day
"""
import httpx
from app.core.config import settings
from app.services.cache import get_or_fetch

ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"


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