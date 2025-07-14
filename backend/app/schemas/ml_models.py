#backend/app/schemas/ml_models.py

from pydantic import BaseModel
from datetime import datetime

class MLModelBase(BaseModel):
    model_name: str
    model_file_path: str

class MLModelCreate(MLModelBase):
    machine_id: int
    created_by: int

class MLModelRead(MLModelBase):
    id: int
    machine_id: int
    created_by: int
    created_at: datetime

class Config:
    from_attributes = True
