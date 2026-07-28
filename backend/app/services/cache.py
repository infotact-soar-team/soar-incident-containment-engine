# backend/app/services/cache.py
import json
from typing import Optional, Callable, Any
from app.core.redis_client import redis_client

DEFAULT_TTL_SECONDS = 3600  # 1 hour


def get_cached(key: str) -> Optional[dict]:
    """Returns cached value as a dict, or None if not present."""
    raw = redis_client.get(key)
    if raw is None:
        return None
    return json.loads(raw)


def set_cached(key: str, value: dict, ttl: int = DEFAULT_TTL_SECONDS) -> None:
    """Stores a dict in Redis with a TTL (default 1 hour)."""
    redis_client.setex(key, ttl, json.dumps(value))


def get_or_fetch(key: str, fetch_fn: Callable[[], Any], ttl: int = DEFAULT_TTL_SECONDS) -> dict:
    """
    Checks cache first; on miss, calls fetch_fn(), caches the result, and returns it.
    """
    cached = get_cached(key)
    if cached is not None:
        return cached

    result = fetch_fn()
    set_cached(key, result, ttl)
    return result


# backend/tests/test_cache.py
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
