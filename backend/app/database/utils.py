import logging

from sqlalchemy.ext.asyncio import AsyncEngine

from app.models import BaseModel
from .session import engine

logger = logging.getLogger(__name__)

async def create_all_tables(engine: AsyncEngine = engine):
    async with engine.begin() as conn:
        logger.info("Create all tables")
        await conn.run_sync(BaseModel.metadata.create_all)
