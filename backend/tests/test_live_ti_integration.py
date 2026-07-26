import os
import pytest
from app.integrations.abuseipdb import check_ip
from app.integrations.virustotal import check_hash
from app.integrations.geoip import lookup_ip_location

# These tests hit REAL external APIs and consume real rate-limit quota.
# Skipped by default; only run when RUN_LIVE_TI_TESTS=1 is set explicitly.
RUN_LIVE = os.getenv("RUN_LIVE_TI_TESTS") == "1"

# A known-public test IP (Google DNS) — safe, well-documented, non-sensitive
TEST_IP = "8.8.8.8"
# EICAR test file hash — the industry-standard "safe test malware" hash
EICAR_HASH = "44d88612fea8a8f36de82e1278abb02f"


@pytest.mark.skipif(not RUN_LIVE, reason="Live TI API test — set RUN_LIVE_TI_TESTS=1 to run")
def test_live_abuseipdb_check():
    result = check_ip(TEST_IP)
    assert "abuse_confidence_score" in result
    assert isinstance(result["abuse_confidence_score"], int)


@pytest.mark.skipif(not RUN_LIVE, reason="Live TI API test — set RUN_LIVE_TI_TESTS=1 to run")
def test_live_virustotal_eicar_hash():
    result = check_hash(EICAR_HASH)
    # EICAR is a known test file — VT should show high malicious detections
    assert result["malicious"] > 0


@pytest.mark.skipif(not RUN_LIVE, reason="Live TI API test — set RUN_LIVE_TI_TESTS=1 to run")
def test_live_geoip_lookup():
    result = lookup_ip_location(TEST_IP)
    assert result["country"] is not None