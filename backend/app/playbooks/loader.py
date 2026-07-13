import yaml
from app.schemas.playbook import PlaybookDefinition

def load_playbook(path: str) -> PlaybookDefinition:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    return PlaybookDefinition(**raw)
