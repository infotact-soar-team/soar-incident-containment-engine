"""
GeoIP Integration using MaxMind GeoLite2 (skeleton - live implementation in Week 2)
Docs: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
Auth: Local .mmdb database file (no API key needed) or GeoIP2 Web Service API key
Rate limit: N/A for local DB; web service has its own quota
"""


def lookup_ip_location(ip: str) -> dict:
    """
    Return country/city/lat-long for a given IP using GeoLite2.
    To be implemented in Week 2.
    """
    raise NotImplementedError("GeoIP live integration pending - Week 2")