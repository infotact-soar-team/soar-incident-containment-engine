# backend/app/core/rate_limiter.py

import time
from collections import defaultdict

# Exception used by callers/tests when rate limits are exceeded
class RateLimitExceeded(Exception):
    """Raised when a rate limit is exceeded."""
    pass

# Simple in-memory rate limiter stub
_last_called = defaultdict(list)

def check_rate_limit(service_name: str, max_requests: int, window_seconds: int) -> bool:
    """
    Temporary stub for rate limiting.
    Allows up to `max_requests` calls per `window_seconds` window.
    """
    now = time.time()
    calls = _last_called[service_name]

    # Remove old timestamps
    _last_called[service_name] = [t for t in calls if now - t < window_seconds]

    if len(_last_called[service_name]) >= max_requests:
        # In real implementation, raise or delay. Keep returning False for backward compatibility.
        return False

    _last_called[service_name].append(now)
    return True
