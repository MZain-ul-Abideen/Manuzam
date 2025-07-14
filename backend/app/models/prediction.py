from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Prediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines.id'))
    audio_file_path = Column(String)
    predicted_label = Column(String)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    machine = relationship("Machine", back_populates="predictions")
