from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_all_tables
from app.api.v1 import routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield

app = FastAPI(title="Fisca API", lifespan=lifespan)

for router in routers:
    app.include_router(router)