from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ActionOut(BaseModel):
    id: str
    action_type: str
    target: Optional[str]
    success: bool
    details: Optional[str]
    executed_at: datetime

    class Config:
        from_attributes = True


class IncidentOut(BaseModel):
    id: str
    alert_id: str
    ioc_id: Optional[str]
    playbook_name: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IncidentListResponse(BaseModel):
    total: int
    incidents: List[IncidentOut]