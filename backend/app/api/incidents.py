from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.incident import Incident
from app.models.action import Action
from app.schemas.incident import IncidentOut, IncidentListResponse, ActionOut
from app.auth.dependencies import require_permission

router = APIRouter()


@router.get("/incidents", response_model=IncidentListResponse)
def list_incidents(
    status: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user: dict = Depends(require_permission("view_incidents")),
):
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == status)

    total = query.count()
    incidents = query.order_by(Incident.created_at.desc()).offset(offset).limit(limit).all()

    return IncidentListResponse(
        total=total,
        incidents=[IncidentOut.model_validate(i) for i in incidents],
    )


@router.get("/incidents/{incident_id}/actions", response_model=list[ActionOut])
def get_incident_actions(
    incident_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(require_permission("view_incidents")),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    actions = db.query(Action).filter(Action.incident_id == incident_id).order_by(Action.executed_at.asc()).all()
    return [ActionOut.model_validate(a) for a in actions]