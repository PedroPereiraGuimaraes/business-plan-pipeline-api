from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Project, ProjectStatus, OnboardingAnswer
from app.schemas.projects import ProjectCreate, ProjectUpdate
from app.dependencies import EntityNotFoundException
from uuid import UUID

# Fixed onboarding questions — must stay in sync with the frontend constant
ONBOARDING_QUESTIONS = [
    "problem",
    "proposed_solution",
    "product_stage",
    "value_proposition",
    "competitive_advantage",
    "team_structure",
    "key_roles",
    "location",
    "available_capital",
    "cost_structure",
]

class ProjectService:
    def create_project(self, db: Session, project: ProjectCreate, user_id: UUID):
        existing_project = db.query(Project).filter(
            Project.user_id == user_id,
            Project.name == project.name
        ).first()
        
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A project with this name already exists."
            )

        db_project = Project(
            name=project.name,
            description=project.description,
            main_sector=project.main_sector,
            business_model=project.business_model,
            user_id=user_id
        )
        db.add(db_project)
        db.flush()  # Get project ID before commit

        # Pre-populate the 10 fixed onboarding answers with empty strings
        for question_label in ONBOARDING_QUESTIONS:
            db.add(OnboardingAnswer(
                project_id=db_project.id,
                question=question_label,
                answer=""
            ))

        db.commit()
        db.refresh(db_project)
        return db_project

    def get_projects(self, db: Session, user_id: UUID):
        return db.query(Project).filter(Project.user_id == user_id).all()

    def get_project(self, db: Session, project_id: UUID, user_id: UUID):
        project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
        if not project:
            raise EntityNotFoundException("Project")
        return project

    def delete_project(self, db: Session, project_id: UUID, user_id: UUID):
        project = self.get_project(db, project_id, user_id)
        db.delete(project)
        db.commit()

    def update_status(self, db: Session, project_id: UUID, status: ProjectStatus):
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.status = status.value
            db.commit()
            db.refresh(project)
        return project
