"""
GeoIP Integration using MaxMind GeoLite2 — live implementation, now cached.
Docs: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
"""
import geoip2.database
import geoip2.errors
from app.core.config import settings
from app.services.cache import get_or_fetch


def _fetch_location(ip: str) -> dict:
    try:
        with geoip2.database.Reader(settings.GEOLITE2_DB_PATH) as reader:
            response = reader.city(ip)
            return {
                "ip": ip,
                "country": response.country.name,
                "country_code": response.country.iso_code,
                "city": response.city.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
            }
    except geoip2.errors.AddressNotFoundError:
        return {
            "ip": ip, "country": None, "country_code": None,
            "city": None, "latitude": None, "longitude": None,
            "note": "IP not found in GeoLite2 database",
        }
    except FileNotFoundError:
        raise FileNotFoundError(
            f"GeoLite2 database not found at {settings.GEOLITE2_DB_PATH}."
        )


def lookup_ip_location(ip: str) -> dict:
    cache_key = f"geoip:ip:{ip}"
    return get_or_fetch(cache_key, lambda: _fetch_location(ip), ttl=86400)
