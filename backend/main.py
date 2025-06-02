# backend/main.py

from fastapi import FastAPI
from app.api import api_router  # Import the grouped router from api/__init__.py

app = FastAPI()

# Register all API routes from app/api
app.include_router(api_router)
