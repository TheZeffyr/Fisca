from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_all_tables
from app.api.v1.users import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield

app = FastAPI(title="Fisca API", lifespan=lifespan)
app.include_router(router)