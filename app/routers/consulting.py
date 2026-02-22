from fastapi import APIRouter, Depends, status
from typing import List
from uuid import UUID
from app.dependencies import Database, CurrentUser
from app.schemas import consulting as schemas
from app.services import consulting as service

router = APIRouter(prefix="/consulting", tags=["Consulting"])
consulting_service = service.ConsultingService()

@router.post("", response_model=schemas.ConsultingRequestResponse)
def create_consulting_request(request: schemas.ConsultingRequestCreate, db: Database, current_user: CurrentUser):
    return consulting_service.create_request(db, request, current_user.id)

@router.get("", response_model=List[schemas.ConsultingRequestResponse])
def read_consulting_requests(db: Database, current_user: CurrentUser):
    return consulting_service.get_requests(db, current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_consulting_request(id: str, db: Database, current_user: CurrentUser):
    consulting_service.delete_request(db, UUID(id), current_user.id)
