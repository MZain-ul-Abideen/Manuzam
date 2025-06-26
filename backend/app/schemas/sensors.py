from pydantic import BaseModel
from typing import Optional

class SensorBase(BaseModel):
    temperature_sensor_enabled: bool
    vibration_sensor_enabled: bool
    temperature_value: Optional[float] = None
    vibration_value: Optional[float] = None

class SensorCreate(SensorBase):
    machine_id: int

class SensorRead(SensorBase):
    id: int
    machine_id: int

    class Config:
        from_attributes = True
