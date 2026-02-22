from fastapi import APIRouter, Depends, status
from typing import List
from uuid import UUID
from app.dependencies import Database, CurrentUser
from app.schemas import projects as schemas
from app.services import projects as service

router = APIRouter(prefix="/projects", tags=["Projects"])
project_service = service.ProjectService()

@router.post("", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Database, current_user: CurrentUser):
    return project_service.create_project(db, project, current_user.id)

@router.get("", response_model=List[schemas.ProjectResponse])
def read_projects(db: Database, current_user: CurrentUser):
    return project_service.get_projects(db, current_user.id)

@router.get("/{id}", response_model=schemas.ProjectResponse)
def read_project(id: UUID, db: Database, current_user: CurrentUser):
    return project_service.get_project(db, id, current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: UUID, db: Database, current_user: CurrentUser):
    project_service.delete_project(db, id, current_user.id)
