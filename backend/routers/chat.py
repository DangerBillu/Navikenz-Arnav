from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.chat import ChatDashboardResponse, ChatDetailResponse, ChatResponse, CreateChatRequest, MessageResponse, SendMessageRequest
from backend.security import get_current_user
from backend.services import chat_services

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(payload: CreateChatRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return chat_services.CreateChat(db, user.id, payload.title)


@router.get("", response_model=list[ChatResponse])
def get_user_chats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return chat_services.GetUserChats(db, user.id)


@router.get("/dashboard", response_model=ChatDashboardResponse)
def get_user_chat_dashboard(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return chat_services.GetDashboardStats(db, user.id)


@router.get("/{chat_id}", response_model=ChatDetailResponse)
def get_chat(chat_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = chat_services.GetUserChat(db, chat_id, user.id)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return chat


@router.delete("/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    deleted = chat_services.DeleteChat(db, chat_id, user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return {"message": "Chat deleted successfully"}


@router.post("/{chat_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(chat_id: int, payload: SendMessageRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    message = chat_services.SendUserMessage(db, chat_id, user.id, payload.content)
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return message
