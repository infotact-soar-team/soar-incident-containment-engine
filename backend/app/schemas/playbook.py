from typing import List, Optional
from pydantic import BaseModel

class PlaybookTrigger(BaseModel):
    risk_score_min: int
    ioc_type: Optional[str] = None

class PlaybookAction(BaseModel):
    type: str
    target: Optional[str] = None
    message: Optional[str] = None

class PlaybookDefinition(BaseModel):
    name: str
    trigger: PlaybookTrigger
    actions: List[PlaybookAction]
from typing import List, Optional
from pydantic import BaseModel

class PlaybookTrigger(BaseModel):
    risk_score_min: int
    ioc_type: Optional[str] = None

class PlaybookAction(BaseModel):
    type: str
    target: Optional[str] = None
    message: Optional[str] = None

class PlaybookDefinition(BaseModel):
    name: str
    trigger: PlaybookTrigger
    actions: List[PlaybookAction]
