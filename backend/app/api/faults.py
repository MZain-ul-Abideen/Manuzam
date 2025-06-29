# backend/app/api/faults.py

import pathlib, shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from app.core.database import async_session
from app import models
from app.schemas import faults

router = APIRouter(prefix="/faults", tags=["Faults"])

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=faults.FaultRead)
async def create_fault(
    machine_id: int = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # 1. Check machine exists
    result = await db.execute(select(models.Machine).filter_by(id=machine_id))
    machine = result.scalar_one_or_none()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    # 2. Prepare directory
    BASE_DIR = pathlib.Path(__file__).parent.parent
    folder_path = BASE_DIR / "Audios" / f"Machine-{machine_id}" / "Training" / "Faulty"
    folder_path.mkdir(parents=True, exist_ok=True)

    # 3. Temporarily save file in memory (for now, no filename assigned)
    temp_file_content = file.file.read()

    # 4. Create Fault DB entry (without file_path first)
    new_fault = models.Fault(
        machine_id=machine_id,
        name=name,
        description=description,
        file_path="",
        uploaded_at=datetime.utcnow()
    )

    db.add(new_fault)
    await db.commit()
    await db.refresh(new_fault)

    # 5. Rename file based on fault ID
    ext = pathlib.Path(file.filename).suffix
    new_filename = f"audio.{machine_id}.{new_fault.id}{ext}"
    new_path = folder_path / new_filename

    # 6. Save file physically
    try:
        with open(new_path, "wb") as f_out:
            f_out.write(temp_file_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File write failed: {e}")

    # 7. Update DB with file path
    new_fault.file_path = str(new_path)
    await db.commit()

    return new_fault


@router.get("/", response_model=list[faults.FaultRead])
async def get_faults(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Fault))
    return result.scalars().all()
 
@router.get("/machine/{machine_id}", response_model=list[faults.FaultRead])
async def get_faults_by_machine(machine_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Fault).where(models.Fault.machine_id == machine_id)
    )
    faults = result.scalars().all()
    if not faults:
        raise HTTPException(status_code=404, detail="No faults found for this machine")
    return faults