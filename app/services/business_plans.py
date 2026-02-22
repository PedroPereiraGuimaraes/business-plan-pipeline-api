import logging
from uuid import UUID
from fastapi import BackgroundTasks
from app.database import SessionLocal
from app.models import BusinessPlan, Project, ProjectStatus, OnboardingAnswer
from app.services.ai_generator import AIGeneratorService
from app.email import email_service

logger = logging.getLogger(__name__)

class BusinessPlanService:
    def __init__(self):
        self.ai_service = AIGeneratorService()

    def generate_plan_background_task(self, project_id: UUID, user_email: str, user_name: str):
        """
        Runs in the background. Creates its own DB Session.
        Note: We don't use BackgroundTasks here for the email because we are already in the background.
        We can just call the private async sender or run it in an asyncio loop,
        but since the email service uses fastmail which is async, let's just 
        re-use the async email scheduling by creating a new throwaway BackgroundTasks.
        """
        db = SessionLocal()
        try:
            logger.info(f"Starting background generation for project {project_id}")
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                logger.error(f"Project not found for task {project_id}")
                return

            answers = db.query(OnboardingAnswer).filter(OnboardingAnswer.project_id == project_id).all()
            
            data = {
                "name": project.name,
                "description": project.description,
                "sector": project.main_sector,
                "businessModel": project.business_model,
                "answers": ""
            }

            if answers:
                answers_text = "\\n".join([f"Q: {ans.question}\\nR: {ans.answer}\\n" for ans in answers])
                data["answers"] = answers_text
            
            # Call AI
            logger.info(f"Calling AI Generator for project {project_id}")
            markdown_plan = self.ai_service.generate_business_plan(data)
            
            logger.info(f"Calling AI Summary for project {project_id}")
            summary = self.ai_service.generate_executive_summary(markdown_plan)

            logger.info(f"Calling AI Analysis for project {project_id}")
            analysis = self.ai_service.generate_advanced_analysis(markdown_plan)
            
            # Save to DB
            logger.info(f"Saving BusinessPlan for project {project_id}")
            
            from app.models.plan import PlanSectionAnalysis

            existing_plan = db.query(BusinessPlan).filter(BusinessPlan.project_id == project_id).first()
            if existing_plan:
                existing_plan.content_markdown = markdown_plan
                existing_plan.executive_summary = summary
                existing_plan.overall_score = analysis.get("overall_score")
                
                # Remote old sections
                db.query(PlanSectionAnalysis).filter(PlanSectionAnalysis.business_plan_id == existing_plan.id).delete()
                
                for sec in analysis.get("sections_analysis", []):
                    section_analysis = PlanSectionAnalysis(
                        business_plan_id=existing_plan.id,
                        section_name=sec.get("section_name", "Unknown section"),
                        score=sec.get("score"),
                        suggestions=sec.get("suggestions", [])
                    )
                    db.add(section_analysis)
                    
            else:
                plan = BusinessPlan(
                    project_id=project_id,
                    content_markdown=markdown_plan,
                    executive_summary=summary,
                    overall_score=analysis.get("overall_score")
                )
                db.add(plan)
                db.flush() # ensure plan has an ID generated before adding sections
                
                for sec in analysis.get("sections_analysis", []):
                    section_analysis = PlanSectionAnalysis(
                        business_plan_id=plan.id,
                        section_name=sec.get("section_name", "Unknown section"),
                        score=sec.get("score"),
                        suggestions=sec.get("suggestions", [])
                    )
                    db.add(section_analysis)
            
            project.status = ProjectStatus.READY.value
            db.commit()

            # Trigger email
            logger.info(f"Scheduling email for {user_email}")
            # To call async FastMail code from a sync thread, use asyncio
            import asyncio
            
            # Use a throwaway loop or wait for the existing one
            try:
                loop = asyncio.get_running_loop()
                # We shouldn't be here since BackgroundTask runs in threadpool
                loop.create_task(self._send_email_async_wrapper(user_email, user_name, project.name, project_id))
            except RuntimeError:
                asyncio.run(self._send_email_async_wrapper(user_email, user_name, project.name, project_id))

        except Exception as e:
            logger.error(f"Failed to generate plan for {project_id}: {str(e)}")
            try:
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    project.status = ProjectStatus.ONBOARDING.value 
                    db.commit()
            except:
                pass
        finally:
            db.close()

    async def _send_email_async_wrapper(self, user_email: str, user_name: str, project_name: str, project_id: UUID):
        try:
            from fastapi_mail import MessageSchema, MessageType
            
            context = {
                "project_name": project_name, 
                "plan_link": f"http://localhost:8000/api/v1/projects/{project_id}/plan"
            }
            template = email_service.env.get_template("project_ready.html")
            html_body = template.render(**context)

            message = MessageSchema(
                subject=f"Plano Pronto: {project_name}",
                recipients=[user_email],
                body=html_body,
                subtype=MessageType.html
            )
            await email_service._send_email_async(message)
        except Exception as e:
             logger.error(f"Failed to send async email inside background task: {e}")
