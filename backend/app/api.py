from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.api import router
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"message": "File saved", "path": file_location}