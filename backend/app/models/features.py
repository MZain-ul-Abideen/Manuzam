# backend/app/models/features.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base

class FeatureSet(Base):
    __tablename__ = "feature_sets"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    normal_csv_path = Column(String, nullable=False)
    faulty_csv_path = Column(String, nullable=True)
    total_faults = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
