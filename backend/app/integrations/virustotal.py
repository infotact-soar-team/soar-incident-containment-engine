"""
VirusTotal Integration — live implementation, now cached.
Docs: https://developers.virustotal.com/reference/overview
Auth: API key via header 'x-apikey'
Rate limit (free tier): 4 requests/min, 500/day
"""

import httpx
from app.core.config import settings
from app.core.rate_limiter import check_rate_limit
from app.services.cache import get_or_fetch

VT_BASE_URL = "https://www.virustotal.com/api/v3"


def _get_headers() -> dict:
    if not settings.VIRUSTOTAL_API_KEY:
        raise ValueError("VIRUSTOTAL_API_KEY is not set in environment/.env")
    return {"x-apikey": settings.VIRUSTOTAL_API_KEY}


def _fetch_hash(file_hash: str) -> dict:
    check_rate_limit("virustotal", max_requests=4, window_seconds=60)
    url = f"{VT_BASE_URL}/files/{file_hash}"
    response = httpx.get(url, headers=_get_headers(), timeout=10)
    response.raise_for_status()
    stats = response.json()["data"]["attributes"]["last_analysis_stats"]
    return {
        "hash": file_hash,
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
        "undetected": stats.get("undetected", 0),
    }


def _fetch_domain(domain: str) -> dict:
    check_rate_limit("virustotal", max_requests=4, window_seconds=60)
    url = f"{VT_BASE_URL}/domains/{domain}"
    response = httpx.get(url, headers=_get_headers(), timeout=10)
    response.raise_for_status()
    stats = response.json()["data"]["attributes"]["last_analysis_stats"]
    return {
        "domain": domain,
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
        "undetected": stats.get("undetected", 0),
    }


def check_hash(file_hash: str) -> dict:
    cache_key = f"virustotal:hash:{file_hash}"
    return get_or_fetch(cache_key, lambda: _fetch_hash(file_hash), ttl=3600)


def check_domain(domain: str) -> dict:
    cache_key = f"virustotal:domain:{domain}"
    return get_or_fetch(cache_key, lambda: _fetch_domain(domain), ttl=3600)
