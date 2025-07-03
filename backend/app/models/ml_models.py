# backend/app/models/ml_models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base  # ✅ correct Base


class MLModel(Base):
    __tablename__ = 'ml_models'

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines.id'))
    model_name = Column(String)
    model_file_path = Column(String)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime)

    machine = relationship("Machine", back_populates="ml_models")
    creator = relationship("User", back_populates="ml_models", foreign_keys=[created_by])
