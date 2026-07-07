from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.chat import (
    ChatDashboardResponse,
    ChatDetailResponse,
    ChatResponse,
    CreateChatRequest,
    MessageResponse,
    SendMessageRequest,
)
from backend.services import chat_services

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(payload: CreateChatRequest, db: Session = Depends(get_db)):
    chat = chat_services.CreateChat(db, payload.user_id, payload.title)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return chat


@router.get("/user/{user_id}", response_model=list[ChatResponse])
def get_user_chats(user_id: int, db: Session = Depends(get_db)):
    return chat_services.GetUserChats(db, user_id)


@router.get("/user/{user_id}/dashboard", response_model=ChatDashboardResponse)
def get_user_chat_dashboard(user_id: int, db: Session = Depends(get_db)):
    stats = chat_services.GetDashboardStats(db, user_id)
    if stats is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return stats


@router.get("/{chat_id}", response_model=ChatDetailResponse)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = chat_services.GetChat(db, chat_id)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return chat


@router.delete("/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    deleted = chat_services.DeleteChat(db, chat_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return {"message": "Chat deleted successfully"}


@router.post("/{chat_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(chat_id: int, payload: SendMessageRequest, db: Session = Depends(get_db)):
    message = chat_services.SendUserMessage(db, chat_id, payload.content)
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return message
