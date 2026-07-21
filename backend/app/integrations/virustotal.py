"""
VirusTotal Integration — live implementation.
Docs: https://developers.virustotal.com/reference/overview
Auth: API key via header 'x-apikey'
Rate limit (free tier): 4 requests/min, 500/day
"""
import httpx
from app.core.config import settings

VT_BASE_URL = "https://www.virustotal.com/api/v3"


def _get_headers() -> dict:
    if not settings.VIRUSTOTAL_API_KEY:
        raise ValueError("VIRUSTOTAL_API_KEY is not set in environment/.env")
    return {"x-apikey": settings.VIRUSTOTAL_API_KEY}


def check_hash(file_hash: str) -> dict:
    """
    Look up a file hash (MD5/SHA1/SHA256) reputation via VirusTotal.
    """
    url = f"{VT_BASE_URL}/files/{file_hash}"
    response = httpx.get(url, headers=_get_headers(), timeout=10)
    response.raise_for_status()
    data = response.json()["data"]
    stats = data["attributes"]["last_analysis_stats"]

    return {
        "hash": file_hash,
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
        "undetected": stats.get("undetected", 0),
    }


def check_domain(domain: str) -> dict:
    """
    Look up a domain's reputation via VirusTotal.
    """
    url = f"{VT_BASE_URL}/domains/{domain}"
    response = httpx.get(url, headers=_get_headers(), timeout=10)
    response.raise_for_status()
    data = response.json()["data"]
    stats = data["attributes"]["last_analysis_stats"]

    return {
        "domain": domain,
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
        "undetected": stats.get("undetected", 0),
    }