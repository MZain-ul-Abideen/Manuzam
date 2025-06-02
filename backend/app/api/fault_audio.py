from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session
from app import models
from app.schemas import fault_audio_samples

router = APIRouter(prefix="/fault_audio_samples", tags=["Fault Audio Samples"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=fault_audio_samples.FaultAudioSampleRead)
async def create_fault_audio_sample(sample: fault_audio_samples.FaultAudioSampleCreate, db: AsyncSession = Depends(get_db)):
    # Check if fault_id exists
    fault = await db.execute(select(models.Fault).filter_by(id=sample.fault_id))
    if not fault.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Fault not found")
    
    # Check if user_id exists
    user = await db.execute(select(models.User).filter_by(id=sample.user_id))
    if not user.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    
    new_sample = models.FaultAudioSample(**sample.dict())
    db.add(new_sample)
    await db.commit()
    await db.refresh(new_sample)
    return new_sample

@router.get("/", response_model=list[fault_audio_samples.FaultAudioSampleRead])
async def get_fault_audio_samples(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.FaultAudioSample))
    return result.scalars().all()