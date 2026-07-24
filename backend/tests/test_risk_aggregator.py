from app.services.risk_aggregator import aggregate_ip_risk, aggregate_hash_or_domain_risk, aggregate_risk


def test_aggregate_ip_risk_high():
    result = {"abuse_confidence_score": 92}
    assert aggregate_ip_risk(result) == 92


def test_aggregate_ip_risk_missing_score_defaults_zero():
    assert aggregate_ip_risk({}) == 0


def test_aggregate_hash_risk_all_malicious():
    vt_result = {"malicious": 60, "suspicious": 0, "harmless": 0, "undetected": 0}
    score = aggregate_hash_or_domain_risk(vt_result)
    assert score == 100


def test_aggregate_hash_risk_mostly_clean():
    vt_result = {"malicious": 1, "suspicious": 1, "harmless": 50, "undetected": 10}
    score = aggregate_hash_or_domain_risk(vt_result)
    assert 0 <= score <= 10


def test_aggregate_hash_risk_no_engines():
    vt_result = {"malicious": 0, "suspicious": 0, "harmless": 0, "undetected": 0}
    assert aggregate_hash_or_domain_risk(vt_result) == 0


def test_aggregate_risk_dispatches_correctly():
    ip_score = aggregate_risk("ip", abuseipdb_result={"abuse_confidence_score": 70})
    hash_score = aggregate_risk("hash", vt_result={"malicious": 30, "suspicious": 0, "harmless": 0, "undetected": 0})

    assert ip_score == 70
    assert hash_score == 100
