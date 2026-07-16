from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.ai_agent import get_assistant_reply
from backend.crud import chat_crud, user_crud


def CreateChat(db: Session, user_id: int, title: str):
    user = user_crud.get_user(db, user_id)
    if user is None:
        return None

    if user.is_guest and user.guest_chat_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have reached the 3-chat guest limit. Please sign in to continue.",
        )

    chat = chat_crud.create_chat(db, user_id, title)
    if user.is_guest:
        user.guest_chat_count += 1
        db.commit()
    return chat
def GetChat(db: Session, chat_id: int):
    return chat_crud.get_chat(db, chat_id)

def GetUserChat(db: Session, chat_id: int, user_id: int):
    chat = chat_crud.get_chat(db, chat_id)
    return chat if chat is not None and chat.user_id == user_id else None

def GetUserChats(db: Session, user_id: int):
    return chat_crud.get_user_chats(db, user_id)

def GetAllChats(db: Session):
    return chat_crud.get_all_chats(db)

def GetDashboardStats(db: Session, user_id: int):
    if user_crud.get_user(db, user_id) is None:
        return None

    return {
        "total_chats": chat_crud.get_user_chat_count(db, user_id),
        "total_messages": chat_crud.get_user_message_count(db, user_id),
    }

def SendUserMessage(db: Session, chat_id: int, user_id: int, content: str):
    user = user_crud.get_user(db, user_id)
    if user is None:
        return None

    if user.is_guest and chat_crud.get_user_message_count(db, user_id) >= 5:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have reached the 5-message guest limit. Please sign in to continue.",
        )

    chat = GetUserChat(db, chat_id, user_id)
    if chat is None:
        return None

    assistant_reply = get_assistant_reply(content, chat.session_id)
    if not assistant_reply:
        assistant_reply = "Sorry, I could not generate a response right now."

    return chat_crud.create_message(db, chat.id, content, assistant_reply)

def DeleteChat(db: Session, chat_id: int, user_id: int):
    if GetUserChat(db, chat_id, user_id) is None:
        return False
    return chat_crud.delete_chat(db, chat_id)
