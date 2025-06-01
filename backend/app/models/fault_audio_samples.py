from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base  # ✅ correct Base
class FaultAudioSample(Base):
    __tablename__ = 'fault_audio_samples'

    id = Column(Integer, primary_key=True)
    fault_id = Column(Integer, ForeignKey('faults.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    file_path = Column(String)
    uploaded_at = Column(DateTime)

    fault = relationship("Fault", back_populates="fault_audio_samples")
    user = relationship("User", back_populates="fault_audio_samples")
    annotations = relationship("FaultAnnotation", back_populates="fault_audio_sample")
