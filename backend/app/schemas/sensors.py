from pydantic import BaseModel

class SensorBase(BaseModel):
    temperature_sensor_enabled: bool
    vibration_sensor_enabled: bool

class SensorCreate(SensorBase):
    machine_id: int

class SensorRead(SensorBase):
    id: int
    machine_id: int

    class Config:
        orm_mode = True
