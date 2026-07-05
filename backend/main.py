from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database.connection import Base, engine
from backend.models import user as user_model
from backend.routers import endpoints

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(endpoints.router)

