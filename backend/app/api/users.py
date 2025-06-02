# app/api/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session
from sqlalchemy import select
from app import models
from app.schemas import users

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/")
async def create_user(user: users.UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User)
    )
    return result.scalars().all()
