"""
AbuseIPDB Integration — live implementation.
Docs: https://docs.abuseipdb.com/
Auth: API key via header 'Key'
Rate limit (free tier): 1,000 checks/day
"""
import httpx
from app.core.config import settings

ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"


def check_ip(ip: str) -> dict:
    """
    Check an IP's abuse confidence score via AbuseIPDB.
    Returns a simplified dict with the fields we care about.
    """
    if not settings.ABUSEIPDB_API_KEY:
        raise ValueError("ABUSEIPDB_API_KEY is not set in environment/.env")

    headers = {
        "Key": settings.ABUSEIPDB_API_KEY,
        "Accept": "application/json",
    }
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