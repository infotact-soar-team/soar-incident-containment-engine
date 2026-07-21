from app.services.cache import get_or_fetch
from app.services.enrichment import enrich_ip


def test_enrichment_result_gets_cached():
    """
    Simulates the Week 2 pattern: wrap an enrichment call in get_or_fetch
    so repeated lookups of the same IoC don't re-trigger expensive calls.
    """
    calls = {"count": 0}

    def fetch_and_count():
        calls["count"] += 1
        result = enrich_ip("185.220.101.1")
        return result.dict()

    key = "enrichment:ip:185.220.101.1"

    first = get_or_fetch(key, fetch_and_count, ttl=60)
    second = get_or_fetch(key, fetch_and_count, ttl=60)

    assert first == second
    assert calls["count"] == 1  # second lookup should hit cache


def test_different_iocs_are_cached_separately():
    def fetch_ip1():
        return enrich_ip("1.2.3.4").dict()

    def fetch_ip2():
        return enrich_ip("5.6.7.8").dict()

    result1 = get_or_fetch("enrichment:ip:1.2.3.4", fetch_ip1, ttl=60)
    result2 = get_or_fetch("enrichment:ip:5.6.7.8", fetch_ip2, ttl=60)

    assert result1["ioc_value"] == "1.2.3.4"
    assert result2["ioc_value"] == "5.6.7.8"