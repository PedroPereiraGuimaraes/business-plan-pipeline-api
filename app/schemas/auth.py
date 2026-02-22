from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID4
    created_at: datetime
    access_level: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[UUID4] = None

class UserPasswordResetRequest(BaseModel):
    email: EmailStr
