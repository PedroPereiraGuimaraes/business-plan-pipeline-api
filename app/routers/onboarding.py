from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from uuid import UUID
from typing import List
from app.dependencies import Database, CurrentUser
from app.schemas import onboarding as schemas
from app.services import onboarding as service
from app.services.projects import ProjectService

router = APIRouter(tags=["Onboarding"])
onboarding_service = service.OnboardingService()
project_service = ProjectService()

@router.get("/projects/{id}/onboarding", response_model=List[schemas.OnboardingAnswerResponse])
def get_onboarding(id: UUID, db: Database, current_user: CurrentUser):
    """Returns the 10 fixed onboarding answers for a project."""
    project_service.get_project(db, id, current_user.id)
    return onboarding_service.get_answers(db, id)

@router.patch("/projects/{id}/onboarding/{question_label}", response_model=schemas.OnboardingAnswerResponse)
def update_single_answer(id: UUID, question_label: str, payload: schemas.OnboardingAnswerUpdate, db: Database, current_user: CurrentUser):
    """Updates a single onboarding answer by its question label."""
    project_service.get_project(db, id, current_user.id)
    return onboarding_service.update_single_answer(db, id, question_label, payload.answer)

@router.post("/projects/{id}/complete")
def complete_onboarding(id: UUID, db: Database, current_user: CurrentUser, background_tasks: BackgroundTasks):
    project_service.get_project(db, id, current_user.id)
    onboarding_service.complete_onboarding(db, id, background_tasks)
    return {"message": "Plan generation started", "status": "generating"}

