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

class MachineRead(MachineBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
