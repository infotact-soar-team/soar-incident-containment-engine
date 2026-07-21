from app.services.risk_mapping import RISK_BANDS, severity_for_score


def test_bands_loaded_from_yaml():
    assert len(RISK_BANDS) == 3
    assert RISK_BANDS[0]["severity"] == "high"


def test_severity_still_works_after_externalizing():
    assert severity_for_score(95) == "high"
    assert severity_for_score(50) == "medium"
    assert severity_for_score(10) == "low"
