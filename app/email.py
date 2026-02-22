from typing import Any, Optional, Dict
import logging
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config import settings
from starlette.background import BackgroundTasks
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

class EmailService:
    def __init__(self):
        template_dir = Path(__file__).parent / "templates" / "email"
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    async def _send_email_async(self, message: MessageSchema):
        fm = FastMail(conf)
        try:
            await fm.send_message(message)
            logger.info(f"Email sent successfully to {message.recipients}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    def _schedule_email(self, background_tasks: BackgroundTasks, subject: str, recipients: list[str], template_name: str, context: Dict[str, Any]):
        template = self.env.get_template(template_name)
        html_body = template.render(**context)

        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=html_body,
            subtype=MessageType.html
        )
        background_tasks.add_task(self._send_email_async, message)

    def send_welcome_email(self, background_tasks: BackgroundTasks, user_email: str, user_name: str):
        subject = "Bem-vindo ao Business Plan Pipeline!"
        self._schedule_email(
            background_tasks, 
            subject, 
            [user_email], 
            "welcome.html", 
            {"user_name": user_name}
        )

    def send_password_reset_email(self, background_tasks: BackgroundTasks, user_email: str, reset_token: str):
        subject = "Redefinição de Senha"
        link = f"https://app.businessplanpipeline.com/reset-password?token={reset_token}"
        self._schedule_email(
            background_tasks, 
            subject, 
            [user_email], 
            "password_reset.html", 
            {"link": link}
        )

    def send_project_ready_email(self, background_tasks: BackgroundTasks, user_email: str, project_name: str, plan_link: str):
        subject = f"Plano Pronto: {project_name}"
        self._schedule_email(
            background_tasks, 
            subject, 
            [user_email], 
            "project_ready.html", 
            {"project_name": project_name, "plan_link": plan_link}
        )

    def send_consulting_scheduled_email(self, background_tasks: BackgroundTasks, user_email: str, meeting_link: str, objective: str):
        subject = "Consultoria Agendada Confirmada"
        self._schedule_email(
            background_tasks, 
            subject, 
            [user_email], 
            "consulting_confirmation.html", 
            {"objective": objective, "meeting_link": meeting_link}
        )

email_service = EmailService()
