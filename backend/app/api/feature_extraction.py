# backend/app/api/feature_extraction.py

import os
import pathlib
import librosa
import pandas as pd
import numpy as np
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import async_session
from app import models
from app.schemas import features as feature_schema

router = APIRouter(prefix="/features", tags=["Feature Extraction"])

async def get_db():
    async with async_session() as session:
        yield session


# Feature Extraction Function
def extract_features(audio_path: str) -> np.ndarray:
    y, sr = librosa.load(audio_path, sr=None)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

    features = np.hstack([
        np.mean(mfcc, axis=1),
        np.mean(chroma, axis=1),
        np.mean(zcr),
        np.mean(spec_centroid)
    ])
    return features


@router.post("/", response_model=feature_schema.FeatureSetOut)
async def generate_feature_csv(
    machine_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Fetch machine to ensure it exists
    result = await db.execute(select(models.Machine).where(models.Machine.id == machine_id))
    machine = result.scalar_one_or_none()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    # Prepare output directories
    base_dir = pathlib.Path(__file__).parent.parent
    feature_dir = base_dir / "features"
    normal_dir = feature_dir / "normal"
    faulty_dir = feature_dir / "faulty"

    normal_dir.mkdir(parents=True, exist_ok=True)
    faulty_dir.mkdir(parents=True, exist_ok=True)

    # === NORMAL AUDIO ===
    normal_audio = await db.execute(
        select(models.NormalAudio).where(models.NormalAudio.machine_id == machine_id)
    )
    normal_audio = normal_audio.scalar_one_or_none()
    if not normal_audio:
        raise HTTPException(status_code=404, detail="No normal audio found")

    normal_path = pathlib.Path(normal_audio.file_path)
    normal_features = extract_features(str(normal_path))

    feature_names = [f"mfcc_{i+1}" for i in range(13)] + \
                    [f"chroma_{i+1}" for i in range(12)] + \
                    ["zcr_mean", "spectral_centroid_mean"]

    df_normal = pd.DataFrame([normal_features], columns=feature_names)
    df_normal.insert(0, "filename", normal_path.name)

    normal_csv_path = normal_dir / f"machine-{machine_id}_normal.csv"
    df_normal.to_csv(normal_csv_path, index=False)

    # === FAULTY AUDIO ===
    result = await db.execute(
        select(models.Fault).where(models.Fault.machine_id == machine_id)
    )
    faulty_audios = result.scalars().all()

    df_faulty = None
    faulty_csv_path = None
    if faulty_audios:
        feature_rows = []
        for fault in faulty_audios:
            fault_path = pathlib.Path(fault.file_path)
            try:
                features = extract_features(str(fault_path))
                row = [fault_path.name] + list(features)
                feature_rows.append(row)
            except Exception as e:
                print(f"❌ Failed to extract fault audio: {fault_path}, Error: {e}")

        if feature_rows:
            df_faulty = pd.DataFrame(feature_rows, columns=["filename"] + feature_names)
            faulty_csv_path = faulty_dir / f"machine-{machine_id}_faulty.csv"
            df_faulty.to_csv(faulty_csv_path, index=False)

    # === Save Metadata in DB ===
    feature_entry = models.features(
        machine_id=machine_id,
        normal_csv_path=str(normal_csv_path),
        faulty_csv_path=str(faulty_csv_path) if faulty_csv_path else None,
        total_faults=len(faulty_audios),
        created_at=datetime.utcnow(),
    )

    db.add(feature_entry)
    await db.commit()
    await db.refresh(feature_entry)

    return feature_entry
