import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from app.database.base import Base
from app.database.types import UUIDType


class EnrichmentResultModel(Base):
    __tablename__ = "enrichment_results"

    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    ioc_id = Column(UUIDType(), ForeignKey("iocs.id"), nullable=False)

    abuse_confidence_score = Column(Integer, nullable=True)
    vt_malicious_count = Column(Integer, nullable=True)
    geo_country = Column(String, nullable=True)
    risk_score = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
