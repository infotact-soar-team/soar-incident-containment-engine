import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class EnrichmentResultModel(Base):
    __tablename__ = "enrichment_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ioc_id = Column(UUID(as_uuid=True), ForeignKey("iocs.id"), nullable=False)

    abuse_confidence_score = Column(Integer, nullable=True)
    vt_malicious_count = Column(Integer, nullable=True)
    geo_country = Column(String, nullable=True)
    risk_score = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)