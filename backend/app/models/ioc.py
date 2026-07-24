import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Index
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class IOC(Base):
    __tablename__ = "iocs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_id = Column(UUID(as_uuid=True), ForeignKey("alerts.id"), nullable=False, index=True)
    ioc_type = Column(String, nullable=False, index=True)
    value = Column(String, nullable=False, index=True)
    enrichment_id = Column(UUID(as_uuid=True), ForeignKey("enrichment_results.id"), nullable=True)
    risk_score = Column(Integer, nullable=True, index=True)
    severity = Column(String, nullable=True, index=True)
    recommended_action = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_iocs_type_value", "ioc_type", "value"),
    )