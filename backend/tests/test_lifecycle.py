import pytest
from app.database.session import SessionLocal
from app.models.alert import Alert
from app.services.lifecycle import transition_alert, InvalidTransitionError


def _create_alert(status="new"):
    db = SessionLocal()
    alert = Alert(source="Splunk", raw_payload="{}", severity="high", status=status)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    alert_id = str(alert.id)
    db.close()
    return alert_id


def test_valid_transition_new_to_enriched():
    alert_id = _create_alert("new")
    result = transition_alert(alert_id, "enriched")
    assert result["new_status"] == "enriched"


def test_invalid_transition_raises():
    alert_id = _create_alert("new")
    with pytest.raises(InvalidTransitionError):
        transition_alert(alert_id, "contained")  # can't skip straight to contained


def test_terminal_state_has_no_further_transitions():
    alert_id = _create_alert("contained")
    with pytest.raises(InvalidTransitionError):
        transition_alert(alert_id, "new")