#backend/app/schemas/normal_audio_samples.py

from pydantic import BaseModel
from datetime import datetime

class NormalAudioSampleBase(BaseModel):
    file_path: str
    title: str 

class NormalAudioSampleCreate(NormalAudioSampleBase):
    machine_id: int

class NormalAudioSampleRead(NormalAudioSampleBase):
    id: int
    machine_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
