import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class Action(Base):
    __tablename__ = "actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id"), nullable=False)
    action_type = Column(String, nullable=False)  # BLOCK_IP / ISOLATE_HOST / AWS_SG_ISOLATE / NOTIFY_ANALYST / LOG_ONLY
    target = Column(String, nullable=True)         # the IP/hostname acted upon
    success = Column(Boolean, default=True)
    details = Column(String, nullable=True)        # raw result/log message
    executed_at = Column(DateTime, default=datetime.utcnow)