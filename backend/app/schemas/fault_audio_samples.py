from pydantic import BaseModel
from datetime import datetime

class FaultAudioSampleBase(BaseModel):
    file_path: str

class FaultAudioSampleCreate(FaultAudioSampleBase):
    fault_id: int
    user_id: int

class FaultAudioSampleRead(FaultAudioSampleBase):
    id: int
    fault_id: int
    user_id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
