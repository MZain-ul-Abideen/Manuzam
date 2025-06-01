from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base  # ✅ correct Base

class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines.id'))
    temperature_sensor_enabled = Column(Boolean)
    vibration_sensor_enabled = Column(Boolean)

    machine = relationship("Machine", back_populates="sensors")
