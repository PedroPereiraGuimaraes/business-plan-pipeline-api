import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from app.database import Base

class ConsultingRequest(Base):
    __tablename__ = "consulting_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    type = Column(String, nullable=False)
    objective = Column(String, nullable=False)
    meeting_link = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("app.models.user.User", backref=backref("consulting_requests", cascade="all, delete-orphan"))
    project = relationship("app.models.project.Project", backref=backref("consulting_requests", cascade="all, delete-orphan"))
