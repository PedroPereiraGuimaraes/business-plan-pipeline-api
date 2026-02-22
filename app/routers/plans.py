from fastapi import APIRouter
from uuid import UUID
from app.dependencies import Database, CurrentUser
from app.schemas import plans as schemas
from app.services import plans as service
from app.services.projects import ProjectService

router = APIRouter(tags=["Plans"])
plan_service = service.PlanService()
project_service = ProjectService()

@router.get("/projects/{id}/plan", response_model=schemas.PlanMarkdownResponse)
def get_plan_markdown(id: UUID, db: Database, current_user: CurrentUser):
    """Returns only the markdown content of the business plan."""
    project_service.get_project(db, id, current_user.id)
    return plan_service.get_plan_by_project(db, id)

@router.get("/projects/{id}/plan/analysis", response_model=schemas.PlanAnalysisResponse)
def get_plan_analysis(id: UUID, db: Database, current_user: CurrentUser):
    """Returns the executive summary, overall score and per-section analysis."""
    project_service.get_project(db, id, current_user.id)
    return plan_service.get_plan_by_project(db, id)
