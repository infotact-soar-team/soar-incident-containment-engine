from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel


class ActionOut(BaseModel):
    id: UUID
    action_type: str
    target: Optional[str]
    success: bool
    details: Optional[str]
    executed_at: datetime

    class Config:
        from_attributes = True


class IncidentOut(BaseModel):
    id: UUID
    alert_id: UUID
    ioc_id: Optional[UUID]
    playbook_name: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IncidentListResponse(BaseModel):
    total: int
    incidents: List[IncidentOut]
