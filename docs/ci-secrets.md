# CI Secrets Reference

The CI pipeline needs these values set under Repo → Settings → Secrets and variables → Actions:

| Secret Name | Purpose | Real value needed? |
|---|---|---|
| ABUSEIPDB_API_KEY_TEST | Lets settings load without error | No — dummy string works, all HTTP calls are mocked in CI |
| VIRUSTOTAL_API_KEY_TEST | Lets settings load without error | No — dummy string works, all HTTP calls are mocked in CI |

`RUN_LIVE_TI_TESTS` is explicitly set to `"0"` in CI so the real live-API tests
(tests/test_live_ti_integration.py) never run automatically and never burn the
team's real free-tier quota.