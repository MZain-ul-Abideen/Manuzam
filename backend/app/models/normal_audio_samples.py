from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base  # ✅ correct Base



class NormalAudioSample(Base):
    __tablename__ = 'normal_audio_samples'

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines.id'), unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_path = Column(String)
    uploaded_at = Column(DateTime)

    machine = relationship("Machine", back_populates="normal_audio_sample")
    user = relationship("User", back_populates="normal_audio_samples")
