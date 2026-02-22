import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from app.database import Base

class ProjectStatus(str, enum.Enum):
    ONBOARDING = "onboarding"
    GENERATING = "generating"
    READY = "ready"

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    main_sector = Column(String, nullable=True)
    business_model = Column(String, nullable=True)
    status = Column(String, default=ProjectStatus.ONBOARDING.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("app.models.user.User", backref=backref("projects", cascade="all, delete-orphan"))
