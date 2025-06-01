import asyncio
from app.core.database import engine, Base  # ✅ import Base from here
from app.models import *  # 👈 ensures models are registered
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # ✅ use correct Base

if __name__ == "__main__":
    asyncio.run(init_db())
