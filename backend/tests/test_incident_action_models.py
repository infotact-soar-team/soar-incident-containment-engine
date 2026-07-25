import uuid
from app.models.incident import Incident
from app.models.action import Action


def test_incident_model_defaults():
    incident = Incident(alert_id=uuid.uuid4())
    assert incident.status == "open"


def test_action_model_defaults():
    action = Action(incident_id=uuid.uuid4(), action_type="BLOCK_IP", target="1.2.3.4")
    assert action.success is True
    assert action.target == "1.2.3.4"