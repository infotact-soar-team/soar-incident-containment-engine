from typing import Optional
from pydantic import BaseModel


class EnrichmentResult(BaseModel):
    ioc_value: str
    ioc_type: str
    abuse_confidence_score: Optional[int] = None
    vt_malicious_count: Optional[int] = None
    geo_country: Optional[str] = None
    risk_score: Optional[int] = None