from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base  # ✅ correct Base
class Fault(Base):
    __tablename__ = 'faults'

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines.id'))
    name = Column(String)
    description = Column(String)

    machine = relationship("Machine", back_populates="faults")
    fault_audio_samples = relationship("FaultAudioSample", back_populates="fault")
