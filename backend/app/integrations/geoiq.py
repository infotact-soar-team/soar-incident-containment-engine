"""
GeoIP Integration using MaxMind GeoLite2 — live implementation.
Docs: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
Requires the GeoLite2-City.mmdb file downloaded locally (path set in .env).
"""
import geoip2.database
import geoip2.errors
from app.core.config import settings


def lookup_ip_location(ip: str) -> dict:
    """
    Return country/city/lat-long for a given IP using the local GeoLite2 database.
    """
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
            "ip": ip,
            "country": None,
            "country_code": None,
            "city": None,
            "latitude": None,
            "longitude": None,
            "note": "IP not found in GeoLite2 database (likely private/reserved IP)",
        }
    except FileNotFoundError:
        raise FileNotFoundError(
            f"GeoLite2 database not found at {settings.GEOLITE2_DB_PATH}. "
            "Download it from https://dev.maxmind.com/geoip/geolite2-free-geolocation-data"
        )