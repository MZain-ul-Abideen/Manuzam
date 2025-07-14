from pydantic import BaseModel
from datetime import datetime

class PredictionBase(BaseModel):
    machine_id: int
    audio_file_path: str
    predicted_label: str
    confidence: float

class PredictionCreate(PredictionBase):
    pass

class PredictionRead(PredictionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
