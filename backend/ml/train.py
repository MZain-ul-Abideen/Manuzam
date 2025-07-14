# backend/ml/train.py

import os
import joblib
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Machine, Sensor, NormalAudioSample, Fault, MLModel
from ml.features import extract_total_features

# Path to store trained models
MODEL_DIR = "ml/saved_models"
os.makedirs(MODEL_DIR, exist_ok=True)


async def train_model_for_machine(machine_id: int, db: AsyncSession):
    # Step 1: Get machine and creator
    result = await db.execute(select(Machine).where(Machine.id == machine_id))
    machine = result.scalar_one_or_none()
    if not machine:
        raise Exception(f"Machine {machine_id} not found.")

    created_by = machine.user_id


    # Step 2: Get sensor data (simplified: latest one)
    result = await db.execute(select(Sensor).where(Sensor.machine_id == machine_id))
    sensor = result.scalars().first()  # You can improve by picking latest or average

    # Convert to dicts
    machine_data = {
        "year_of_installation": machine.year_of_installation,
        "expected_lifespan": machine.expected_lifespan,
        "operating_hours_per_day": machine.operating_hours_per_day
    }

    sensor_data = {
        "temperature_value": sensor.temperature_value if sensor else 0.0,
        "vibration_value": sensor.vibration_value if sensor else 0.0
    }

    # Step 3: Collect audio samples
    X = []
    y = []

    # Normal samples
    result = await db.execute(select(NormalAudioSample).where(NormalAudioSample.machine_id == machine_id))
    normal_samples = result.scalars().all()
    for sample in normal_samples:
        features = extract_total_features(sample.file_path, machine_data, sensor_data)
        label = sample.title if sample.title else "normal"
        X.append(features)
        y.append(label)


    # Faulty samples
    result = await db.execute(select(Fault).where(Fault.machine_id == machine_id))
    fault_samples = result.scalars().all()
    for fault in fault_samples:
        features = extract_total_features(fault.file_path, machine_data, sensor_data)
        X.append(features)
        y.append(fault.name)  # Using fault.name as label

    if len(X) < 2:
        raise Exception("Not enough data to train a model.")

    # Step 4: Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(np.array(X), np.array(y))

    # Step 5: Save model
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    model_name = f"machine_{machine_id}_{timestamp}.joblib"
    model_path = os.path.join(MODEL_DIR, model_name)
    joblib.dump(model, model_path)

    # Step 6: Save metadata to DB
    new_model_entry = MLModel(
        machine_id=machine_id,
        model_name=model_name,
        model_file_path=model_path,
        created_by=created_by,
        created_at=datetime.utcnow()
    )
    db.add(new_model_entry)
    
    machine.machine_trained = True
    
    await db.commit()

    return {"message": "Model trained successfully.", "model_path": model_path}
