# backend/app/schemas/users.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password_hash: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True