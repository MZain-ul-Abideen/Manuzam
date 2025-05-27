from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router  # Assuming your API code is in api.py

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
