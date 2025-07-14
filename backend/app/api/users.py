# backend/app/api/users.py

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

@router.post("/", response_model=users.UserOut)
async def create_user(user: users.UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user with email already exists
    existing_user = await db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Check if username already exists
    existing_username = await db.execute(
        select(models.User).where(models.User.username == user.username)
    )
    if existing_username.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[users.UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User).order_by(models.User.created_at.desc())
    )
    return result.scalars().all()

@router.get("/{user_id}", response_model=users.UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=users.UserOut)
async def update_user(user_id: int, user_update: users.UserUpdate, db: AsyncSession = Depends(get_db)):
    # Get existing user
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if new email is already taken by another user
    if user_update.email and user_update.email != existing_user.email:
        email_check = await db.execute(
            select(models.User).where(
                models.User.email == user_update.email,
                models.User.id != user_id
            )
        )
        if email_check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already taken by another user")
    
    # Check if new username is already taken by another user
    if user_update.username and user_update.username != existing_user.username:
        username_check = await db.execute(
            select(models.User).where(
                models.User.username == user_update.username,
                models.User.id != user_id
            )
        )
        if username_check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already taken by another user")
    
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_user, field, value)
    
    await db.commit()
    await db.refresh(existing_user)
    return existing_user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(models.User).where(models.User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        await db.delete(user)
        await db.commit()
        return {"message": "User deleted successfully"}

    except Exception as e:
        # Log the error
        print(f"Error deleting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
