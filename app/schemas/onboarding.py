from pydantic import BaseModel, UUID4
from typing import List

class OnboardingAnswerCreate(BaseModel):
    question: str
    answer: str

class OnboardingAnswerResponse(OnboardingAnswerCreate):
    id: UUID4
    project_id: UUID4
    
    class Config:
        from_attributes = True

class OnboardingCompletion(BaseModel):
    success: bool
    message: str
