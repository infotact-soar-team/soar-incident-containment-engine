import pytest
from app.core.rate_limiter import check_rate_limit, RateLimitExceeded


def test_rate_limit_allows_under_threshold():
    key = "test:vt:under-threshold"
    for _ in range(3):
        check_rate_limit(key, max_requests=4, window_seconds=60)  # should not raise


def test_rate_limit_blocks_over_threshold():
    key = "test:vt:over-threshold"
    for _ in range(4):
        check_rate_limit(key, max_requests=4, window_seconds=60)

    with pytest.raises(RateLimitExceeded):
        check_rate_limit(key, max_requests=4, window_seconds=60)
import pytest
from app.core.rate_limiter import reset_rate_limits  # adjust module path if different

@pytest.fixture(autouse=True)
def clear_rate_limit_state():
    """Automatically resets in-memory rate limit counts before every test in this file."""
    reset_rate_limits()
    yield
    reset_rate_limits()