# app/schemas/users.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password_hash: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

class Config:
    from_attributes = True
