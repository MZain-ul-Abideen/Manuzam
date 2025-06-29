from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import os, shutil

from app.core.database import async_session
from app import models
from app.schemas import normal_audio_samples
import pathlib

router = APIRouter(prefix="/normal_audio_samples", tags=["Normal Audio Samples"])

async def get_db():
    async with async_session() as session:
        yield session


@router.get("/", response_model=list[normal_audio_samples.NormalAudioSampleRead])
async def get_all_normal_audio_samples(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.NormalAudioSample))
    samples = result.scalars().all()
    return samples


@router.get("/machine/{machine_id}", response_model=list[normal_audio_samples.NormalAudioSampleRead])
async def get_normal_audio_samples_by_machine(machine_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.NormalAudioSample).where(models.NormalAudioSample.machine_id == machine_id)
    )
    samples = result.scalars().all()
    if not samples:
        raise HTTPException(status_code=404, detail="No normal audio samples found for this machine")
    return samples

@router.post("/", response_model=normal_audio_samples.NormalAudioSampleRead)
async def upload_normal_audio_sample(
    machine_id: int = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # 1. Check machine exists
    result = await db.execute(select(models.Machine).where(models.Machine.id == machine_id))
    machine = result.scalar_one_or_none()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    # 2. Prepare directory
    BASE_DIR = pathlib.Path(__file__).parent.parent
    folder_path = BASE_DIR / "Audios" / f"Machine-{machine_id}" / "Training" / "Normal"
    folder_path.mkdir(parents=True, exist_ok=True)

    ext = pathlib.Path(file.filename).suffix
    filename = f"normal_audio_{machine_id}{ext}"
    file_path = folder_path / filename

    # 3. Optional cleanup: delete previous file + DB row
    existing = await db.execute(
        select(models.NormalAudioSample).where(models.NormalAudioSample.machine_id == machine_id)
    )
    existing_sample = existing.scalars().first()
    if existing_sample:
        try:
            os.remove(existing_sample.file_path)
        except Exception as e:
            print(f"Warning: Failed to delete old file: {e}")
        await db.delete(existing_sample)
        await db.commit()

    # 4. Save file to disk
    try:
        with open(file_path, "wb") as out_file:
            shutil.copyfileobj(file.file, out_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # 5. Add to DB
    audio_sample = models.NormalAudioSample(
        machine_id=machine_id,
        file_path=str(file_path),
        uploaded_at=datetime.utcnow()
    )
    db.add(audio_sample)
    await db.commit()
    await db.refresh(audio_sample)

    return audio_sample
