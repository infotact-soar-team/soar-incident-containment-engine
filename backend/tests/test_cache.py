
from app.services.cache import get_or_fetch, get_cached, set_cached


def test_set_and_get_cached():
    set_cached("test:key1", {"foo": "bar"}, ttl=60)
    result = get_cached("test:key1")
    assert result == {"foo": "bar"}


def test_get_cached_missing_key():
    result = get_cached("test:nonexistent-key-xyz")
    assert result is None


def test_get_or_fetch_calls_fetch_on_miss():
    calls = {"count": 0}

    def fetch():
        calls["count"] += 1
        return {"value": 42}

    # First call should trigger fetch()
    result1 = get_or_fetch("test:key2", fetch, ttl=60)
    # Second call should hit cache, not fetch again
    result2 = get_or_fetch("test:key2", fetch, ttl=60)

    assert result1 == {"value": 42}
    assert result2 == {"value": 42}
    assert calls["count"] == 1
