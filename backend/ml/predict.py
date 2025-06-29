import os
import joblib
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sklearn.base import ClassifierMixin
from sklearn.exceptions import NotFittedError

from app.models import Machine, Sensor, MLModel
from ml.features import extract_total_features


async def predict_for_machine(
    machine_id: int,
    audio_path: str,
    sensor_data: dict,
    db: AsyncSession
):
    # Step 1: Get machine metadata
    result = await db.execute(select(Machine).where(Machine.id == machine_id))
    machine = result.scalar_one_or_none()
    if not machine:
        raise Exception(f"Machine {machine_id} not found.")

    machine_data = {
        "year_of_installation": machine.year_of_installation,
        "expected_lifespan": machine.expected_lifespan,
        "operating_hours_per_day": machine.operating_hours_per_day
    }

    # Step 2: Get latest model for this machine
    result = await db.execute(
        select(MLModel)
        .where(MLModel.machine_id == machine_id)
        .order_by(MLModel.created_at.desc())
        .limit(1)
    )
    model_entry = result.scalar_one_or_none()
    if not model_entry:
        raise Exception("No trained model found for this machine.")

    model_path = model_entry.model_file_path
    if not os.path.exists(model_path):
        raise Exception("Model file not found at path: " + model_path)

    model: ClassifierMixin = joblib.load(model_path)

    # Step 3: Extract features from new data
    features = extract_total_features(audio_path, machine_data, sensor_data).reshape(1, -1)

    # Step 4: Predict label
    try:
        predicted_label = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        labels = model.classes_

        # Build confidence scores for all known faults/normal
        confidence_scores = dict(zip(labels, probabilities))

        return {
            "predicted_label": predicted_label,
            "confidence_scores": confidence_scores
        }

    except NotFittedError:
        raise Exception("Model was not fitted properly.")

