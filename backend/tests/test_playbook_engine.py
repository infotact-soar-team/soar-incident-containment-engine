from app.playbooks.loader import load_playbook
from app.playbooks.engine import PlaybookEngine


def test_playbook_engine_executes_all_steps_in_order():
    """
    Verify that all actions in the playbook are executed in order
    and return success results.
    """
    playbook = load_playbook("backend/app/playbooks/definitions/example_playbook.yaml")
    engine = PlaybookEngine(playbook)

    results = engine.execute("185.220.101.1")

    # Example playbook has BLOCK_IP and NOTIFY_ANALYST
    assert len(results) == 2
    assert results[0]["action"] == "BLOCK_IP"
    assert results[0]["success"] is True
    assert results[1]["action"] == "NOTIFY_ANALYST"
    assert results[1]["success"] is True


def test_playbook_engine_substitutes_ioc_value_in_message():
    """
    Ensure IoC value is correctly substituted into analyst notification messages.
    """
    playbook = load_playbook("backend/app/playbooks/definitions/example_playbook.yaml")
    engine = PlaybookEngine(playbook)

    results = engine.execute("1.2.3.4")
    notify_result = next(r for r in results if r["action"] == "NOTIFY_ANALYST")
    assert "1.2.3.4" in notify_result["message"]
    assert notify_result["success"] is True


def test_playbook_engine_handles_unknown_action_type():
    """
    Verify that unknown action types are handled gracefully with error.
    """
    # Construct a fake playbook with an invalid action type
    class FakeStep:
        def __init__(self):
            self.type = "UNKNOWN_ACTION"
            self.message = None

    class FakePlaybook:
        actions = [FakeStep()]

    engine = PlaybookEngine(FakePlaybook())
    results = engine.execute("dummy-ioc")

    assert results[0]["action"] == "UNKNOWN_ACTION"
    assert results[0]["success"] is False
    assert "error" in results[0]


def test_playbook_engine_supports_all_action_dispatch_types():
    """
    Ensure all supported action types return success when executed.
    """
    from app.schemas.playbook import PlaybookDefinition, PlaybookAction

    actions = [
        PlaybookAction(type="BLOCK_IP", message=None),
        PlaybookAction(type="ISOLATE_HOST", message=None),
        PlaybookAction(type="AWS_SG_ISOLATE", message=None),
        PlaybookAction(type="NOTIFY_ANALYST", message="Notify about {{ ioc_value }}"),
        PlaybookAction(type="LOG_ONLY", message=None),
    ]
    playbook = PlaybookDefinition(
        name="Dispatch Test",
        trigger={"risk_score_min": 0, "ioc_type": "ip"},
        actions=actions
    )
    engine = PlaybookEngine(playbook)

    results = engine.execute("9.9.9.9")

    assert len(results) == 5
    for r in results:
        assert r["success"] is True
