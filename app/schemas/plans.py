from pydantic import BaseModel, UUID4
from typing import Dict, Any, List, Optional
from datetime import datetime

class PlanSectionAnalysisBase(BaseModel):
    section_name: str
    score: Optional[int]
    suggestions: Optional[List[str]]

    class Config:
        from_attributes = True

class PlanResponse(BaseModel):
    id: UUID4
    project_id: UUID4
    content_markdown: Optional[str]
    executive_summary: Optional[str]
    overall_score: Optional[int]
    sections: List[PlanSectionAnalysisBase] = []
    created_at: datetime
    
    class Config:
        from_attributes = True
