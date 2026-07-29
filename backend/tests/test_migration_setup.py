from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_alembic_folder_exists():
    assert (BACKEND_ROOT / "alembic").is_dir()


def test_alembic_ini_exists():
    assert (BACKEND_ROOT / "alembic.ini").is_file()
