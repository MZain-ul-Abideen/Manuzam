# backend/app/api/normal_audio.py

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session
from app import models
from app.schemas import normal_audio_samples
import os
import shutil

# ✅ Define router before using it
router = APIRouter(prefix="/normal_audio_samples", tags=["Normal Audio Samples"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

# Your existing @router.post("/") and @router.get("/") go here...

# ✅ Upload endpoint
@router.post("/upload", response_model=normal_audio_samples.NormalAudioSampleRead)
async def upload_normal_audio_sample(
    machine_id: int = Form(...),
    user_id: int = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # DB existence checks
    machine = await db.execute(select(models.Machine).filter_by(id=machine_id))
    if not machine.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Machine not found")

    user = await db.execute(select(models.User).filter_by(id=user_id))
    if not user.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")

    # Save file
    upload_dir = "uploads/"
    os.makedirs(upload_dir, exist_ok=True)
    file_location = os.path.join(upload_dir, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Create DB record
    new_sample = models.NormalAudioSample(
        machine_id=machine_id,
        user_id=user_id,
        description=description,
        file_path=file_location  # adjust this field based on your model
    )
    db.add(new_sample)
    await db.commit()
    await db.refresh(new_sample)
    return new_sample
