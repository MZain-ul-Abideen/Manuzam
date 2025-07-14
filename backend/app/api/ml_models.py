# backend/app/api/ml_models.py
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

@router.get("/", response_model=list[ml_models.MLModelRead])
async def get_ml_models(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.MLModel))
    return result.scalars().all()

@router.get("/{model_id}", response_model=ml_models.MLModelRead)
async def get_ml_model_by_id(model_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.MLModel).where(models.MLModel.id == model_id))
    ml_model = result.scalar_one_or_none()
    if not ml_model:
        raise HTTPException(status_code=404, detail="ML Model not found")
    return ml_model


@router.post("/train/{machine_id}")
async def train_machine_model(machine_id: int, db: AsyncSession = Depends(get_db)):
    try:
        from ml.train import train_model_for_machine
        result = await train_model_for_machine(machine_id=machine_id, db=db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
