from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NormalizedAlert(BaseModel):
    source: str
    severity: str
    message: str
    timestamp: datetime
    raw_source_field: Optional[str] = None