# backend/app/core/rate_limiter.py

import time
from collections import defaultdict

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
        # In real implementation, raise or delay
        return False

    _last_called[service_name].append(now)
    return True
