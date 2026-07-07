from sqlalchemy.orm import Session, joinedload

from backend.models.chat_session import ChatSession
from backend.models.message import Message


def create_chat(db: Session, user_id: int, title: str):
    chat = ChatSession(user_id=user_id, title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chat(db: Session, chat_id: int):
    return (
        db.query(ChatSession)
        .options(joinedload(ChatSession.messages))
        .filter(ChatSession.id == chat_id)
        .first()
    )


def get_user_chats(db: Session, user_id: int):
    return (
        db.query(ChatSession)
        .options(joinedload(ChatSession.messages))
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )


def get_all_chats(db: Session):
    return (
        db.query(ChatSession)
        .options(joinedload(ChatSession.messages))
        .order_by(ChatSession.created_at.desc())
        .all()
    )


def get_user_chat_count(db: Session, user_id: int):
    return db.query(ChatSession).filter(ChatSession.user_id == user_id).count()


def get_user_message_count(db: Session, user_id: int):
    return (
        db.query(Message)
        .join(ChatSession, Message.chat_session_id == ChatSession.id)
        .filter(ChatSession.user_id == user_id)
        .count()
    )


def delete_chat(db: Session, chat_id: int):
    chat = get_chat(db, chat_id)
    if chat is None:
        return False

    db.delete(chat)
    db.commit()
    return True


def create_message(db: Session, chat_session_id: int, sent_message: str, received_message: str):
    message = Message(
        chat_session_id=chat_session_id,
        sent_message=sent_message,
        received_message=received_message,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
