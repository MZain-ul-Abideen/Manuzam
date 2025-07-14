# schemas/faults.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FaultBase(BaseModel):
    name: str
    description: str
    file_path: Optional[str] = None
    uploaded_at: Optional[datetime] = None

class FaultCreate(FaultBase):
    machine_id: int

class FaultRead(FaultBase):
    id: int
    machine_id: int

    class Config:
        from_attributes = True
