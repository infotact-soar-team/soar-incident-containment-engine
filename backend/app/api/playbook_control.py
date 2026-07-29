from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.incident import Incident
from app.models.ioc import IOC
from app.auth.dependencies import require_permission
from app.playbooks.loader import load_playbook
from app.playbooks.engine import PlaybookEngine
from app.services.incident_service import log_actions
from app.tasks.enrichment_task import PLAYBOOK_FILE_MAP

router = APIRouter()


@router.post("/incidents/{incident_id}/rerun")
def rerun_playbook(
    incident_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(require_permission("rerun_playbook")),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    if not incident.playbook_name or incident.playbook_name not in PLAYBOOK_FILE_MAP:
        raise HTTPException(status_code=400, detail="No known playbook to re-run for this incident")

    ioc = db.query(IOC).filter(IOC.id == incident.ioc_id).first()
    if not ioc:
        raise HTTPException(status_code=400, detail="Original IoC not found")

    playbook = load_playbook(PLAYBOOK_FILE_MAP[incident.playbook_name])
    engine = PlaybookEngine(playbook)
    results = engine.execute(ioc.value)

    log_actions(incident_id, results)

    return {
        "incident_id": incident_id,
        "rerun_by": user["username"],
        "actions_taken": len(results),
        "results": results,
    }
