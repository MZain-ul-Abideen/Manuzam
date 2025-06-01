from pydantic import BaseModel
from datetime import datetime

class FaultAnnotationBase(BaseModel):
    cause: str
    confirmed: bool

class FaultAnnotationCreate(FaultAnnotationBase):
    fault_audio_sample_id: int
    user_id: int

class FaultAnnotationRead(FaultAnnotationBase):
    id: int
    fault_audio_sample_id: int
    user_id: int
    annotated_at: datetime

    class Config:
        orm_mode = True
