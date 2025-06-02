from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session
from app import models
from app.schemas import fault_annotations

router = APIRouter(prefix="/fault_annotations", tags=["Fault Annotations"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=fault_annotations.FaultAnnotationRead)
async def create_fault_annotation(annotation: fault_annotations.FaultAnnotationCreate, db: AsyncSession = Depends(get_db)):
    # Check if fault_audio_sample_id exists
    fault_audio_sample = await db.execute(select(models.FaultAudioSample).filter_by(id=annotation.fault_audio_sample_id))
    if not fault_audio_sample.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Fault audio sample not found")
    
    # Check if user_id exists
    user = await db.execute(select(models.User).filter_by(id=annotation.user_id))
    if not user.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    
    new_annotation = models.FaultAnnotation(**annotation.dict())
    db.add(new_annotation)
    await db.commit()
    await db.refresh(new_annotation)
    return new_annotation

@router.get("/", response_model=list[fault_annotations.FaultAnnotationRead])
async def get_fault_annotations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.FaultAnnotation))
    return result.scalars().all()