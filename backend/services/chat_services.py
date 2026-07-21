from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.ai_agent import get_assistant_reply
from backend.crud import chat_crud, user_crud

GUEST_CHAT_LIMIT = 3
GUEST_MESSAGE_LIMIT = 5


def create_chat(db: Session, user_id: int, title: str):
    user = user_crud.get_user(db, user_id)
    if user is None:
        return None

    if user.is_guest and user.guest_chat_count >= GUEST_CHAT_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You have reached the {GUEST_CHAT_LIMIT}-chat guest limit. Please sign up to continue.",
        )

    chat = chat_crud.create_chat(db, user_id, title)
    if user.is_guest:
        user.guest_chat_count += 1
        db.commit()
    return chat


def get_chat(db: Session, chat_id: int):
    return chat_crud.get_chat(db, chat_id)


def get_user_chat(db: Session, chat_id: int, user_id: int):
    chat = chat_crud.get_chat(db, chat_id)
    return chat if chat is not None and chat.user_id == user_id else None


def get_user_chats(db: Session, user_id: int):
    return chat_crud.get_user_chats(db, user_id)


def get_all_chats(db: Session):
    return chat_crud.get_all_chats(db)


def get_dashboard_stats(db: Session, user_id: int):
    if user_crud.get_user(db, user_id) is None:
        return None

    return {
        "total_chats": chat_crud.get_user_chat_count(db, user_id),
        "total_messages": chat_crud.get_user_message_count(db, user_id),
    }


def send_user_message(db: Session, chat_id: int, user_id: int, content: str):
    user = user_crud.get_user(db, user_id)
    if user is None:
        return None

    if user.is_guest and chat_crud.get_user_message_count(db, user_id) >= GUEST_MESSAGE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You have reached the {GUEST_MESSAGE_LIMIT}-message guest limit. Please sign up to continue.",
        )

    chat = get_user_chat(db, chat_id, user_id)
    if chat is None:
        return None

    assistant_reply = get_assistant_reply(content, chat.session_id)
    if not assistant_reply:
        assistant_reply = "Sorry, I could not generate a response right now."

    return chat_crud.create_message(db, chat.id, content, assistant_reply)


def delete_chat(db: Session, chat_id: int, user_id: int):
    if get_user_chat(db, chat_id, user_id) is None:
        return False
    return chat_crud.delete_chat(db, chat_id)
