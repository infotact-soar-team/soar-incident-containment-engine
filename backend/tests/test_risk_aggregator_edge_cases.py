from app.services.risk_aggregator import aggregate_ip_risk, aggregate_hash_or_domain_risk, aggregate_risk


def test_aggregate_ip_risk_clamps_above_100():
    result = {"abuse_confidence_score": 150}  # malformed/unexpected upstream data
    assert aggregate_ip_risk(result) == 100


def test_aggregate_ip_risk_clamps_below_zero():
    result = {"abuse_confidence_score": -10}
    assert aggregate_ip_risk(result) == 0


def test_aggregate_hash_risk_only_suspicious_no_malicious():
    vt_result = {"malicious": 0, "suspicious": 20, "harmless": 20, "undetected": 0}
    score = aggregate_hash_or_domain_risk(vt_result)
    assert 20 <= score <= 30  # suspicious weighted at 0.5x


def test_aggregate_hash_risk_mixed_signals():
    vt_result = {"malicious": 10, "suspicious": 5, "harmless": 30, "undetected": 5}
    score = aggregate_hash_or_domain_risk(vt_result)
    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_aggregate_risk_unknown_ioc_type_returns_zero():
    assert aggregate_risk("url", vt_result={"malicious": 50}) == 0


def test_aggregate_risk_missing_kwargs_does_not_crash():
    # No enrichment data passed at all — should not raise
    assert aggregate_risk("ip") == 0
    assert aggregate_risk("hash") == 0
