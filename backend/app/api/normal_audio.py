from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session
from app import models
from app.schemas import normal_audio_samples

router = APIRouter(prefix="/normal_audio_samples", tags=["Normal Audio Samples"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=normal_audio_samples.NormalAudioSampleRead)
async def create_normal_audio_sample(sample: normal_audio_samples.NormalAudioSampleCreate, db: AsyncSession = Depends(get_db)):
    # Check if machine_id exists
    machine = await db.execute(select(models.Machine).filter_by(id=sample.machine_id))
    if not machine.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Machine not found")
    
    # Check if user_id exists
    user = await db.execute(select(models.User).filter_by(id=sample.user_id))
    if not user.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    
    new_sample = models.NormalAudioSample(**sample.dict())
    db.add(new_sample)
    await db.commit()
    await db.refresh(new_sample)
    return new_sample

@router.get("/", response_model=list[normal_audio_samples.NormalAudioSampleRead])
async def get_normal_audio_samples(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.NormalAudioSample))
    return result.scalars().all()