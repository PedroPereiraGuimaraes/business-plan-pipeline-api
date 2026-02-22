from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import Database, CurrentUser
from app.schemas import auth as schemas
from app.services import auth as service

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = service.AuthService()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Database, background_tasks: BackgroundTasks):
    return auth_service.create_user(db, user, background_tasks)

@router.post("/login", response_model=schemas.Token)
def login(db: Database, form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.create_access_token(
        data={"sub": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: CurrentUser):
    return current_user

@router.post("/forgot-password")
def forgot_password(request: schemas.UserPasswordResetRequest, db: Database, background_tasks: BackgroundTasks):
    auth_service.request_password_reset(db, request.email, background_tasks)
    return {"message": "If the email exists, a reset link was sent."}

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Database, current_user: CurrentUser):
    auth_service.delete_user(db, current_user)
