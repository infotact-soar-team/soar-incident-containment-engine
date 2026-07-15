def test_abuseipdb_fixture_shape(mock_abuseipdb_response):
    assert "data" in mock_abuseipdb_response
    assert "abuseConfidenceScore" in mock_abuseipdb_response["data"]


def test_virustotal_hash_fixture_shape(mock_virustotal_hash_response):
    stats = mock_virustotal_hash_response["data"]["attributes"]["last_analysis_stats"]
    assert "malicious" in stats


def test_geoip_fixture_shape(mock_geoip_response):
    assert "country" in mock_geoip_response
    assert "latitude" in mock_geoip_response