from pathlib import Path

import yaml

from app.schemas.playbook import PlaybookDefinition


def load_playbook(path: str) -> PlaybookDefinition:
    base_dir = Path(__file__).resolve().parent.parent
    repo_root = base_dir.parent
    candidate = Path(path)

    if not candidate.is_absolute():
        candidates = [
            (base_dir / candidate).resolve(),
            (repo_root / candidate).resolve(),
        ]
        existing = next((c for c in candidates if c.exists()), None)
        if existing is None:
            raise FileNotFoundError(f"Playbook file not found: {path}")
        candidate = existing

    with candidate.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if not isinstance(raw, dict):
        raise ValueError(f"Playbook YAML must contain a mapping at the top level: {path}")

    return PlaybookDefinition(**raw)
