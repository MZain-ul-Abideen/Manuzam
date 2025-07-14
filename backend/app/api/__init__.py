# backend/app/api/__init__.py

from fastapi import APIRouter
from . import users, machine, ml_models, faults, sensors, normal_audio, predict

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(machine.router)
api_router.include_router(ml_models.router)
api_router.include_router(faults.router)
api_router.include_router(sensors.router)
api_router.include_router(normal_audio.router)
api_router.include_router(predict.router)
