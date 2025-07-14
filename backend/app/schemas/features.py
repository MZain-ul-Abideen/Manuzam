from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeatureSetOut(BaseModel):
    id: int
    machine_id: int
    normal_csv_path: str
    faulty_csv_path: Optional[str]
    total_faults: int
    created_at: datetime

    class Config:
        orm_mode = True
