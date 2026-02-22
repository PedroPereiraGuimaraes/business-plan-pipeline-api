from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from app.models import ProjectStatus

class ProjectBase(BaseModel):
    name: str
    description: str
    main_sector: str
    business_model: str

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    main_sector: Optional[str] = None
    business_model: Optional[str] = None
    status: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: UUID4
    user_id: UUID4
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
