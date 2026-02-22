from sqlalchemy.orm import Session
from app.models import ConsultingRequest, Project, User
from app.schemas.consulting import ConsultingRequestCreate
from app.dependencies import EntityNotFoundException
from uuid import UUID
import random
import string
from app.email import email_service
from fastapi import BackgroundTasks

class ConsultingService:
    def create_request(self, db: Session, request: ConsultingRequestCreate, user_id: UUID, background_tasks: BackgroundTasks):
        # Verify project ownership/existence
        project = db.query(Project).filter(Project.id == request.project_id, Project.user_id == user_id).first()
        if not project:
             raise EntityNotFoundException("Project")
             
        # Generate Fake Meet Link
        # Format: xxx-xxx-xxx
        meeting_code = '-'.join([''.join(random.choices(string.ascii_lowercase, k=3)) for _ in range(3)])
        meeting_link = f"https://meet.google.com/{meeting_code}"
             
        db_request = ConsultingRequest(
            user_id=user_id,
            project_id=request.project_id,
            type=request.type,
            objective=request.objective,
            meeting_link=meeting_link
        )
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        
        # Simulate sending email
        user = db.query(User).filter(User.id == user_id).first()
        email_service.send_consulting_scheduled_email(background_tasks, user.email, meeting_link, request.objective)
        
        return db_request


    def get_requests(self, db: Session, user_id: UUID):
        return db.query(ConsultingRequest).filter(ConsultingRequest.user_id == user_id).all()

    def delete_request(self, db: Session, request_id: UUID, user_id: UUID):
        request = db.query(ConsultingRequest).filter(ConsultingRequest.id == request_id, ConsultingRequest.user_id == user_id).first()
        if not request:
            raise EntityNotFoundException("Consulting Request")
        db.delete(request)
        db.commit()
