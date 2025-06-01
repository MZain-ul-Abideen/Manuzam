from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base  # ✅ correct Base

class FaultAnnotation(Base):
    __tablename__ = 'fault_annotations'

    id = Column(Integer, primary_key=True)
    fault_audio_sample_id = Column(Integer, ForeignKey('fault_audio_samples.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    cause = Column(String)
    confirmed = Column(Boolean)
    annotated_at = Column(DateTime)

    fault_audio_sample = relationship("FaultAudioSample", back_populates="annotations")
    user = relationship("User", back_populates="fault_annotations")
