import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String, nullable=False)
    raw_payload = Column(String, nullable=False)
    severity = Column(String, default="unknown", index=True)
    status = Column(String, default="new", index=True)
    received_at = Column(DateTime, default=datetime.utcnow, index=True)
    normalized_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("ix_alerts_severity_status", "severity", "status"),
    )