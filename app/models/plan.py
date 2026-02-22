import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Text, Integer, String
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from app.database import Base

class BusinessPlan(Base):
    __tablename__ = "business_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, unique=True)
    
    # Structured fields
    content_markdown = Column(Text, nullable=True)
    executive_summary = Column(Text, nullable=True)
    overall_score = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("app.models.project.Project", backref=backref("business_plan", uselist=False, cascade="all, delete-orphan"))
    sections = relationship("PlanSectionAnalysis", back_populates="business_plan", cascade="all, delete-orphan")

class PlanSectionAnalysis(Base):
    __tablename__ = "plan_section_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    business_plan_id = Column(UUID(as_uuid=True), ForeignKey("business_plans.id"), nullable=False)
    section_name = Column(String, nullable=False)
    score = Column(Integer, nullable=True)
    suggestions = Column(ARRAY(String), nullable=True)

    business_plan = relationship("BusinessPlan", back_populates="sections")
