from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean, Float
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base  # ✅ correct Base

class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines.id', ondelete="CASCADE"), nullable=False)  # <-- Fix here
    temperature_sensor_enabled = Column(Boolean)
    vibration_sensor_enabled = Column(Boolean)
    temperature_value = Column(Float)
    vibration_value = Column(Float)

    machine = relationship("Machine", back_populates="sensors")
