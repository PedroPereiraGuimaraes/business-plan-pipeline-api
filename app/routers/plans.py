from fastapi import APIRouter, Depends
from uuid import UUID
from app.dependencies import Database, CurrentUser
from app.schemas import plans as schemas
from app.services import plans as service
from app.services.projects import ProjectService

router = APIRouter(tags=["Plans"])
plan_service = service.PlanService()
project_service = ProjectService()

@router.get("/projects/{id}/plan", response_model=schemas.PlanResponse)
def get_project_plan(id: UUID, db: Database, current_user: CurrentUser):
    # Verify ownership
    project_service.get_project(db, id, current_user.id)
    return plan_service.get_plan_by_project(db, id)
