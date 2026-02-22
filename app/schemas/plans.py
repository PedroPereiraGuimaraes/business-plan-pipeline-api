from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime

class PlanSectionAnalysisBase(BaseModel):
    section_name: str
    score: Optional[int]
    suggestions: Optional[List[str]]

    class Config:
        from_attributes = True

class PlanMarkdownResponse(BaseModel):
    """Returns only the markdown content of the plan."""
    id: UUID4
    project_id: UUID4
    content_markdown: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class PlanAnalysisResponse(BaseModel):
    """Returns the executive summary and advanced analysis (scores + suggestions)."""
    id: UUID4
    project_id: UUID4
    executive_summary: Optional[str]
    overall_score: Optional[int]
    sections: List[PlanSectionAnalysisBase] = []
    created_at: datetime

    class Config:
        from_attributes = True
