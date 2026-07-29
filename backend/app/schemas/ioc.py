from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class IOCOut(BaseModel):
    id: str
    alert_id: str
    ioc_type: str
    value: str
    risk_score: Optional[int]
    severity: Optional[str]
    recommended_action: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True