from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session
from ml.predict import predict_for_machine
import shutil
import pathlib
import os
import uuid
import json
from app.models import Prediction
from app.schemas.prediction import PredictionRead  # You need to create this if not already

router = APIRouter(prefix="/predict", tags=["Prediction"])

async def get_db():
    async with async_session() as session:
        yield session

@router.get("/", response_model=list[PredictionRead])
async def get_all_predictions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Prediction))
    predictions = result.scalars().all()
    return predictions

@router.get("/machine/{machine_id}", response_model=list[PredictionRead])
async def get_predictions_by_machine(machine_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Prediction).where(Prediction.machine_id == machine_id)
    )
    predictions = result.scalars().all()
    return predictions


@router.post("/")
async def predict(
    machine_id: int = Form(...),
    file: UploadFile = File(...),
    sensor_data: str = Form(...),  # JSON stringified
    db: AsyncSession = Depends(get_db)
):
    try:
        # Parse sensor_data from JSON
        sensor = json.loads(sensor_data)

        # Save uploaded file temporarily
        ext = pathlib.Path(file.filename).suffix
        filename = f"predict_{uuid.uuid4().hex}{ext}"
        temp_path = pathlib.Path("ml/temp_uploads")
        temp_path.mkdir(parents=True, exist_ok=True)
        file_path = temp_path / filename

        with open(file_path, "wb") as out_file:
            shutil.copyfileobj(file.file, out_file)

        # Run prediction
        result = await predict_for_machine(
            machine_id=machine_id,
            audio_path=str(file_path),
            sensor_data=sensor,
            db=db
        )
        
        pred = Prediction(
            machine_id=machine_id,
            audio_file_path=str(file_path),
            predicted_label=result['predicted_label'],
            confidence=result['confidence_scores'][result['predicted_label']]
        )
        db.add(pred)
        await db.commit()
        await db.refresh(pred)


        # Optional: delete file after use
        try:
            os.remove(file_path)
        except Exception:
            pass

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
