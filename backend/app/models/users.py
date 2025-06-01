from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base  # ✅ correct Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    created_at = Column(DateTime)

    machines = relationship("Machine", back_populates="user")
    normal_audio_samples = relationship("NormalAudioSample", back_populates="user")
    fault_audio_samples = relationship("FaultAudioSample", back_populates="user")
    fault_annotations = relationship("FaultAnnotation", back_populates="user")
    ml_models = relationship("MLModel", back_populates="creator", foreign_keys="MLModel.created_by")
