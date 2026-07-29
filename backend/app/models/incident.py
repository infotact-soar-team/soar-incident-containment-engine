import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.database.base import Base
from app.database.types import UUIDType


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    alert_id = Column(UUIDType(), ForeignKey("alerts.id"), nullable=False)
    ioc_id = Column(UUIDType(), ForeignKey("iocs.id"), nullable=True)
    playbook_name = Column(String, nullable=True)
    status = Column(String, default="open", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        # Ensure in-memory defaults when instantiated directly in Python/tests
        kwargs.setdefault("status", "open")
        kwargs.setdefault("id", uuid.uuid4())
        super().__init__(**kwargs)