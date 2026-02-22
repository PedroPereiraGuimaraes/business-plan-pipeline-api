from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from uuid import UUID
from typing import List
from app.dependencies import Database, CurrentUser
from app.schemas import onboarding as schemas
from app.services import onboarding as service
from app.services.projects import ProjectService

router = APIRouter(tags=["Onboarding"])
onboarding_service = service.OnboardingService()
project_service = ProjectService() # To verify ownership

@router.post("/projects/{id}/onboarding", response_model=List[schemas.OnboardingAnswerResponse])
def submit_onboarding(id: UUID, answers: List[schemas.OnboardingAnswerCreate], db: Database, current_user: CurrentUser):
    # Verify project belongs to user
    project_service.get_project(db, id, current_user.id)
    return onboarding_service.save_answers(db, id, answers)

@router.post("/projects/{id}/complete")
def complete_onboarding(id: UUID, db: Database, current_user: CurrentUser, background_tasks: BackgroundTasks):
    # Verify project belongs to user
    project_service.get_project(db, id, current_user.id)
    onboarding_service.complete_onboarding(db, id, background_tasks)
    return {"message": "Plan generation started", "status": "generating"}
