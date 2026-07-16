from contextlib import asynccontextmanager
from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.config import settings
from backend.database.connection import (
    check_database_connection,
    engine,
    ensure_chat_schema,
    ensure_message_schema,
    ensure_user_schema,
    reset_guest_limits,
)
from backend.models.chat_session import ChatSession
from backend.models.message import Message
from backend.models.user import User
from backend.routers import chat, users


@asynccontextmanager
async def lifespan(_app: FastAPI):
    check_database_connection()
    User.metadata.create_all(bind=engine)
    ChatSession.metadata.create_all(bind=engine)
    Message.metadata.create_all(bind=engine)
    ensure_user_schema()
    ensure_chat_schema()
    ensure_message_schema()
    reset_guest_limits()
    yield


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
