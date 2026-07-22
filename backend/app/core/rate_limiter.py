"""
Redis-backed sliding-window rate limiter shared across all TI integrations.
Prevents exceeding free-tier API quotas (e.g. VirusTotal's 4 req/min).
"""
import time
from app.core.redis_client import redis_client


class RateLimitExceeded(Exception):
    pass


def check_rate_limit(key: str, max_requests: int, window_seconds: int) -> None:
    """
    Raises RateLimitExceeded if more than max_requests have been made
    under this key within the last window_seconds.
    Call this before making any external TI API call.
    """
    redis_key = f"ratelimit:{key}"
    now = time.time()
    window_start = now - window_seconds

    redis_client.zremrangebyscore(redis_key, 0, window_start)
    current_count = redis_client.zcard(redis_key)

    if current_count >= max_requests:
        raise RateLimitExceeded(
            f"Rate limit exceeded for '{key}': {current_count}/{max_requests} in {window_seconds}s"
        )

    redis_client.zadd(redis_key, {str(now): now})
    redis_client.expire(redis_key, window_seconds)