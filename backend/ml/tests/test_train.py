import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_maker
from ml.train import train_model_for_machine

async def main():
    async with async_session_maker() as session:
        machine_id = 1  # Replace with a real machine ID
        created_by = 1  # Replace with a real user ID
        try:
            result = await train_model_for_machine(machine_id, session, created_by)
            print("✅ Model trained and saved!")
            print(result)
        except Exception as e:
            print("❌ Error during training:", str(e))

if __name__ == "__main__":
    asyncio.run(main())
