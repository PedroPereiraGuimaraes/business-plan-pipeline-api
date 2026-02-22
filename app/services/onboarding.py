from sqlalchemy.orm import Session
from app.models import OnboardingAnswer, BusinessPlan, Project, ProjectStatus
from app.schemas.onboarding import OnboardingAnswerCreate
from app.dependencies import EntityNotFoundException
from uuid import UUID
from fastapi import BackgroundTasks
from app.services.business_plans import BusinessPlanService

class OnboardingService:
    def __init__(self):
        self.business_plan_service = BusinessPlanService()

    def get_answers(self, db: Session, project_id: UUID):
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise EntityNotFoundException("Project")
        return db.query(OnboardingAnswer).filter(OnboardingAnswer.project_id == project_id).all()

    def update_single_answer(self, db: Session, project_id: UUID, question_label: str, new_answer: str):
        answer = db.query(OnboardingAnswer).filter(
            OnboardingAnswer.project_id == project_id,
            OnboardingAnswer.question == question_label
        ).first()
        if not answer:
            raise EntityNotFoundException("Onboarding Answer")
        answer.answer = new_answer
        db.commit()
        db.refresh(answer)
        return answer

    def save_answers(self, db: Session, project_id: UUID, answers: list[OnboardingAnswerCreate]):
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise EntityNotFoundException("Project")
            
        created_answers = []
        for ans in answers:
            db_answer = OnboardingAnswer(
                project_id=project_id,
                question=ans.question,
                answer=ans.answer
            )
            db.add(db_answer)
            created_answers.append(db_answer)
        
        db.commit()
        return created_answers

    def update_answers(self, db: Session, project_id: UUID, answers: list[OnboardingAnswerCreate]):
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise EntityNotFoundException("Project")

        # Delete all existing answers and replace with new ones
        db.query(OnboardingAnswer).filter(OnboardingAnswer.project_id == project_id).delete()

        updated_answers = []
        for ans in answers:
            db_answer = OnboardingAnswer(
                project_id=project_id,
                question=ans.question,
                answer=ans.answer
            )
            db.add(db_answer)
            updated_answers.append(db_answer)

        db.commit()
        return updated_answers
        
    def complete_onboarding(self, db: Session, project_id: UUID, background_tasks: BackgroundTasks):
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise EntityNotFoundException("Project")
            
        project.status = ProjectStatus.GENERATING.value
        db.commit()
        
        user_email = project.user.email if project.user else ""
        user_name = project.user.name if project.user else ""

        background_tasks.add_task(
            self.business_plan_service.generate_plan_background_task,
            project.id,
            user_email,
            user_name
        )
        
        return True
