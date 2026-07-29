import os


def test_dashboard_wireframe_doc_exists():
    assert os.path.isfile("../docs/dashboard-wireframe.md") or os.path.isfile("docs/dashboard-wireframe.md")