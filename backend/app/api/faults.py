from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session
from app import models
from app.schemas import faults

router = APIRouter(prefix="/faults", tags=["Faults"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=faults.FaultRead)
async def create_fault(fault: faults.FaultCreate, db: AsyncSession = Depends(get_db)):
    # Check if machine_id exists
    machine = await db.execute(select(models.Machine).filter_by(id=fault.machine_id))
    if not machine.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Machine not found")
    
    new_fault = models.Fault(**fault.dict())
    db.add(new_fault)
    await db.commit()
    await db.refresh(new_fault)
    return new_fault

@router.get("/", response_model=list[faults.FaultRead])
async def get_faults(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Fault))
    return result.scalars().all()