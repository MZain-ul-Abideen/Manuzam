from pydantic import BaseModel

class FaultBase(BaseModel):
    name: str
    description: str

class FaultCreate(FaultBase):
    machine_id: int

class FaultRead(FaultBase):
    id: int
    machine_id: int

    class Config:
        orm_mode = True
