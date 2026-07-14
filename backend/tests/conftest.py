import pytest


@pytest.fixture
def mock_abuseipdb_response():
    return {
        "data": {
            "ipAddress": "185.220.101.1",
            "abuseConfidenceScore": 92,
            "countryCode": "DE",
            "totalReports": 145,
        }
    }


@pytest.fixture
def mock_virustotal_hash_response():
    return {
        "data": {
            "id": "44d88612fea8a8f36de82e1278abb02f",
            "attributes": {
                "last_analysis_stats": {
                    "malicious": 58,
                    "suspicious": 2,
                    "undetected": 12,
                    "harmless": 0,
                }
            },
        }
    }


@pytest.fixture
def mock_virustotal_domain_response():
    return {
        "data": {
            "id": "malicious-domain-example.com",
            "attributes": {
                "last_analysis_stats": {
                    "malicious": 15,
                    "suspicious": 3,
                    "undetected": 60,
                    "harmless": 5,
                }
            },
        }
    }


@pytest.fixture
def mock_geoip_response():
    return {
        "ip": "185.220.101.1",
        "country": "Germany",
        "country_code": "DE",
        "city": "Berlin",
        "latitude": 52.5200,
        "longitude": 13.4050,
    }