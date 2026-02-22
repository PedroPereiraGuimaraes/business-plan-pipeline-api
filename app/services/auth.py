from sqlalchemy.orm import Session
from app.models import User
from app.schemas.auth import UserCreate
from app.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status
from datetime import timedelta
from app.email import email_service
from fastapi import BackgroundTasks

class AuthService:
    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, user: UserCreate, background_tasks: BackgroundTasks):
        if self.get_user_by_email(db, user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            name=user.name,
            password_hash=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Send Welcome Email
        email_service.send_welcome_email(background_tasks, db_user.email, db_user.name)
        
        return db_user

    def authenticate_user(self, db: Session, email: str, password: str):
        user = self.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    def request_password_reset(self, db: Session, email: str, background_tasks: BackgroundTasks):
        user = self.get_user_by_email(db, email)
        if user:
            # Generate fake token (simulation)
            token = "dummy-reset-token-123"
            email_service.send_password_reset_email(background_tasks, user.email, token)

    def delete_user(self, db: Session, user: User):
        """Delete a user and all associated data."""
        # SQLAlchemy cascade="all, delete-orphan" on relationships should handle children.
        # But we ensure we are deleting the object attached to the session.
        db.delete(user)
        db.commit()
