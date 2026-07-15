from app.services.normalizer import normalize_alert


def test_normalize_alert_basic():
    raw = {"source": "Splunk", "severity": "critical", "message": "Malware detected", "timestamp": "2026-07-14T10:00:00"}
    result = normalize_alert(raw)
    assert result.source == "Splunk"
    assert result.severity == "high"
    assert result.message == "Malware detected"


def test_normalize_alert_missing_fields():
    raw = {"source": "Wazuh"}
    result = normalize_alert(raw)
    assert result.severity == "low"
    assert result.message == "No message provided"


def test_normalize_alert_unknown_severity():
    raw = {"source": "CustomSIEM", "severity": "banana", "message": "test"}
    result = normalize_alert(raw)
    assert result.severity == "low"