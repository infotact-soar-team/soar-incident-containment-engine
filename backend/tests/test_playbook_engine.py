from app.playbooks.loader import load_playbook
from app.playbooks.engine import PlaybookEngine


def test_playbook_engine_executes_all_steps_in_order():
    playbook = load_playbook("app/playbooks/definitions/example_playbook.yaml")
    engine = PlaybookEngine(playbook)

    results = engine.execute("185.220.101.1")

    assert len(results) == 2  # BLOCK_IP and NOTIFY_ANALYST from example_playbook.yaml
    assert results[0]["success"] is True
    assert results[1]["success"] is True


def test_playbook_engine_substitutes_ioc_value_in_message():
    playbook = load_playbook("app/playbooks/definitions/example_playbook.yaml")
    engine = PlaybookEngine(playbook)

    results = engine.execute("1.2.3.4")
    notify_result = next(r for r in results if r["action"] == "NOTIFY_ANALYST")
    assert "1.2.3.4" in notify_result["message"]
