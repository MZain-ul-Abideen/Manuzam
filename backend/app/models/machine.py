from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Machine(Base):
    __tablename__ = 'machines'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    manufacturer = Column(String)
    model_number = Column(String)
    year_of_installation = Column(Integer)
    operating_hours_per_day = Column(Integer)
    maintenance_schedule = Column(String)
    last_maintenance_date = Column(Date)
    expected_lifespan = Column(Integer)
    machine_trained = Column(Boolean, default=False)  # <-- ✅ New column
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="machines")
    sensors = relationship("Sensor", back_populates="machine", uselist=False, cascade="all, delete", passive_deletes=True)
    normal_audio_sample = relationship("NormalAudioSample", back_populates="machine", uselist=False)
    faults = relationship("Fault", back_populates="machine")
    ml_models = relationship("MLModel", back_populates="machine")
    predictions = relationship("Prediction", back_populates="machine")
