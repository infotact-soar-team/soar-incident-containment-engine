from app.services.risk_mapping import severity_for_score, action_for_score


def test_high_risk_score():
    assert severity_for_score(95) == "high"
    assert action_for_score(95) == "AUTO_CONTAIN"


def test_medium_risk_score():
    assert severity_for_score(50) == "medium"
    assert action_for_score(50) == "NOTIFY_ANALYST"


def test_low_risk_score():
    assert severity_for_score(10) == "low"
    assert action_for_score(10) == "LOG_ONLY"


def test_boundary_scores():
    assert severity_for_score(71) == "high"
    assert severity_for_score(70) == "medium"
    assert severity_for_score(31) == "medium"
    assert severity_for_score(30) == "low"
