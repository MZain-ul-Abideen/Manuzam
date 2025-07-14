from pydantic import BaseModel
from datetime import datetime, date

class MachineBase(BaseModel):
    name: str
    manufacturer: str
    model_number: str
    year_of_installation: int
    operating_hours_per_day: int
    maintenance_schedule: str
    last_maintenance_date: date
    expected_lifespan: int

class MachineCreate(MachineBase):
    user_id: int

class MachineUpdate(BaseModel):
    name: str | None = None
    manufacturer: str | None = None
    model_number: str | None = None
    year_of_installation: int | None = None
    operating_hours_per_day: int | None = None
    maintenance_schedule: str | None = None
    last_maintenance_date: date | None = None
    expected_lifespan: int | None = None
    machine_trained: bool | None = None

class MachineRead(MachineBase):
    id: int
    user_id: int
    machine_trained: bool
    created_at: datetime

    class Config:
        from_attributes = True
