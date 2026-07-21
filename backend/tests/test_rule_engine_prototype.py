from app.services.rule_engine import evaluate_alert


def test_evaluate_high_risk_ip():
    result = evaluate_alert(risk_score=95, ioc_value="185.220.101.1", ioc_type="ip")
    assert result["severity"] == "high"
    assert result["recommended_action"] == "AUTO_CONTAIN"


def test_evaluate_medium_risk_domain():
    result = evaluate_alert(risk_score=50, ioc_value="suspicious-site.com", ioc_type="domain")
    assert result["severity"] == "medium"
    assert result["recommended_action"] == "NOTIFY_ANALYST"


def test_evaluate_low_risk_hash():
    result = evaluate_alert(risk_score=5, ioc_value="abc123", ioc_type="hash")
    assert result["severity"] == "low"
    assert result["recommended_action"] == "LOG_ONLY"


def test_evaluate_multiple_dummy_alerts():
    """Simulates a batch of dummy enrichment results being fed through the engine."""
    dummy_alerts = [
        {"risk_score": 85, "ioc_value": "1.2.3.4", "ioc_type": "ip"},
        {"risk_score": 20, "ioc_value": "safe-site.com", "ioc_type": "domain"},
        {"risk_score": 60, "ioc_value": "def456", "ioc_type": "hash"},
    ]
    results = [evaluate_alert(**a) for a in dummy_alerts]

    assert results[0]["severity"] == "high"
    assert results[1]["severity"] == "low"
    assert results[2]["severity"] == "medium"
