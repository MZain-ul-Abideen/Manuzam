from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session
from app import models
from app.schemas import ml_models

router = APIRouter(prefix="/ml_models", tags=["ML Models"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=ml_models.MLModelRead)
async def create_ml_model(model: ml_models.MLModelCreate, db: AsyncSession = Depends(get_db)):
    # Check if machine_id exists
    machine = await db.execute(select(models.Machine).filter_by(id=model.machine_id))
    if not machine.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Machine not found")
    
    # Check if created_by (user_id) exists
    user = await db.execute(select(models.User).filter_by(id=model.created_by))
    if not user.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    
    new_model = models.MLModel(**model.dict())
    db.add(new_model)
    await db.commit()
    await db.refresh(new_model)
    return new_model

@router.get("/", response_model=list[ml_models.MLModelRead])
async def get_ml_models(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.MLModel))
    return result.scalars().all()