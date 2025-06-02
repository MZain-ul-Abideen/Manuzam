from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session
from app import models
from app.schemas import machine

router = APIRouter(prefix="/machines", tags=["Machines"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=machine.MachineRead)
async def create_machine(machine: machine.MachineCreate, db: AsyncSession = Depends(get_db)):
    # Check if user_id exists
    user = await db.execute(select(models.User).filter_by(id=machine.user_id))
    if not user.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    
    new_machine = models.Machine(**machine.dict())
    db.add(new_machine)
    await db.commit()
    await db.refresh(new_machine)
    return new_machine

@router.get("/", response_model=list[machine.MachineRead])
async def get_machines(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Machine))
    return result.scalars().all()