import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from app.database.base import Base
from app.database.types import UUIDType


class Action(Base):
    __tablename__ = "actions"

    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    incident_id = Column(UUIDType(), ForeignKey("incidents.id"), nullable=False)
    action_type = Column(String, nullable=False)  # BLOCK_IP / ISOLATE_HOST / AWS_SG_ISOLATE / NOTIFY_ANALYST / LOG_ONLY
    target = Column(String, nullable=True)         # the IP/hostname acted upon
    success = Column(Boolean, default=True, nullable=False)
    details = Column(String, nullable=True)        # raw result/log message
    executed_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        kwargs.setdefault("success", True)
        kwargs.setdefault("id", uuid.uuid4())
        super().__init__(**kwargs)