import os


def test_alembic_folder_exists():
    assert os.path.isdir("alembic")


def test_alembic_ini_exists():
    assert os.path.isfile("alembic.ini")