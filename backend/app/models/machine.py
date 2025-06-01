from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base  # ✅ correct Base
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
    created_at = Column(DateTime)

    user = relationship("User", back_populates="machines")
    sensors = relationship("Sensor", back_populates="machine", uselist=False)
    normal_audio_sample = relationship("NormalAudioSample", back_populates="machine", uselist=False)
    faults = relationship("Fault", back_populates="machine")
    ml_models = relationship("MLModel", back_populates="machine")
