import asyncio

from app.database import create_all_tables



async def main():
    await create_all_tables()

asyncio.run(main())