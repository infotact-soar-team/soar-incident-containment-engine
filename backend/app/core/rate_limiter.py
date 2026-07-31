# backend/app/core/rate_limiter.py

import time
from collections import defaultdict

class RateLimitExceeded(Exception):
    """Raised when a rate limit is exceeded."""
    pass

# Global in-memory call history tracker
_last_called = defaultdict(list)

def reset_rate_limits():
    """Utility to clear cached timestamps between test runs."""
    _last_called.clear()

def check_rate_limit(service_name: str, max_requests: int, window_seconds: int) -> bool:
    """
    Checks rate limits for a given service key.
    Raises RateLimitExceeded if max_requests is met or exceeded within window_seconds.
    """
    now = time.time()
    calls = _last_called[service_name]

    # Remove timestamps older than the sliding window
    _last_called[service_name] = [t for t in calls if now - t < window_seconds]

    # If limit reached, raise exception
    if len(_last_called[service_name]) >= max_requests:
        raise RateLimitExceeded(f"Rate limit of {max_requests} requests per {window_seconds}s exceeded for '{service_name}'")

    _last_called[service_name].append(now)
    return True