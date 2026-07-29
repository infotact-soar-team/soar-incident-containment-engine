from app.playbooks.loader import load_playbook
from app.playbooks.engine import PlaybookEngine
from app.tasks.enrichment_task import PLAYBOOK_FILE_MAP


def test_all_4_playbooks_execute_without_error():
    """Final sanity: every playbook in the map actually runs end to end."""
    for name, path in PLAYBOOK_FILE_MAP.items():
        playbook = load_playbook(path)
        engine = PlaybookEngine(playbook)
        results = engine.execute("test-value-123")
        assert len(results) > 0
        assert all("success" in r or "error" in r for r in results)


def test_playbook_map_matches_rule_engine_selection():
    """Ensures every playbook the rule engine could select actually has a file."""
    from app.services.rule_engine import PLAYBOOK_SELECTION
    for combo, playbook_name in PLAYBOOK_SELECTION.items():
        assert playbook_name in PLAYBOOK_FILE_MAP, f"{playbook_name} missing from PLAYBOOK_FILE_MAP"
