# app/api/sensors.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session
from app import models
from app.schemas import sensors

router = APIRouter(prefix="/sensors", tags=["Sensors"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=sensors.SensorRead)
async def create_sensor(sensor: sensors.SensorCreate, db: AsyncSession = Depends(get_db)):
    # Check if machine_id exists (assuming Machine model exists)
    machine = await db.execute(select(models.Machine).filter_by(id=sensor.machine_id))
    if not machine.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Machine not found")
    
    new_sensor = models.Sensor(**sensor.dict())
    db.add(new_sensor)
    await db.commit()
    await db.refresh(new_sensor)
    return new_sensor

@router.get("/", response_model=list[sensors.SensorRead])
async def get_sensors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Sensor))
    return result.scalars().all()
