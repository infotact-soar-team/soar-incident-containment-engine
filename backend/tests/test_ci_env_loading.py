import os


def test_run_live_ti_tests_defaults_off_in_ci():
    # Confirms CI explicitly disables live tests via env var
    if os.getenv("CI") or os.getenv("GITHUB_ACTIONS"):
        assert os.getenv("RUN_LIVE_TI_TESTS") != "1"