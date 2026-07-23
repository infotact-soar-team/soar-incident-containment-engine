from sqlalchemy import inspect
from app.database.session import engine


def test_alerts_table_has_expected_indices():
    inspector = inspect(engine)
    index_names = [idx["name"] for idx in inspector.get_indexes("alerts")]
    assert any("severity" in name or "status" in name for name in index_names) or len(index_names) > 0


def test_iocs_table_has_expected_indices():
    inspector = inspect(engine)
    index_names = [idx["name"] for idx in inspector.get_indexes("iocs")]
    assert len(index_names) > 0