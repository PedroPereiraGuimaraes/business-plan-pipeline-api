from sqlalchemy.orm import Session
from app.models import BusinessPlan
from app.dependencies import EntityNotFoundException
from uuid import UUID

class PlanService:
    def get_plan_by_project(self, db: Session, project_id: UUID):
        plan = db.query(BusinessPlan).filter(BusinessPlan.project_id == project_id).first()
        if not plan:
            raise EntityNotFoundException("Business Plan")
        return plan
