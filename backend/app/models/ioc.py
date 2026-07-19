import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class IOC(Base):
    __tablename__ = "iocs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_id = Column(UUID(as_uuid=True), ForeignKey("alerts.id"), nullable=False)
    ioc_type = Column(String, nullable=False)
    value = Column(String, nullable=False)
    enrichment_id = Column(UUID(as_uuid=True), ForeignKey("enrichment_results.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)