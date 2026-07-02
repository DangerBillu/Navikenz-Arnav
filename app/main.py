from fastapi import FastAPI
from app.routers import endpoints

app = FastAPI()

app.include_router(endpoints.router)

