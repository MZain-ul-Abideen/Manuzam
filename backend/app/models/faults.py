# models/faults.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Fault(Base):
    __tablename__ = 'faults'

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines.id'))
    name = Column(String)
    description = Column(String)
    file_path = Column(String, nullable=True)
    uploaded_at = Column(DateTime, nullable=True)

    machine = relationship("Machine", back_populates="faults")
