from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.database.connection import Base, engine
from backend.app.models import user as user_model
from backend.app.routers import endpoints

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(endpoints.router)

