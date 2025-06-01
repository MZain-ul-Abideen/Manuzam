from fastapi import FastAPI
from app.api import users, machine, ml_models, faults, sensors, normal_audio, fault_audio, annotations  # add your routers here

app = FastAPI()

# Register routers
app.include_router(users.router)
app.include_router(machine.router)
app.include_router(ml_models.router)
app.include_router(faults.router)
app.include_router(normal_audio.router)
app.include_router(sensors.router)
app.include_router(fault_audio.router)
app.include_router(annotations.router)
