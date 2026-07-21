import uuid
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from backend.models.chat_session import ChatSession
from backend.models.message import Message


def _is_default_chat_title(title: str):
    return title.strip().lower() == "new chat"


def _number_default_chat(chat: ChatSession):
    if _is_default_chat_title(chat.title):
        chat.title = f"Chat {chat.user_chat_number}"
        return True

    return False


def create_chat(db: Session, user_id: int, title: str):
    # Calculate the next chat number for this user
    max_chat_number = db.query(func.max(ChatSession.user_chat_number)).filter(
        ChatSession.user_id == user_id
    ).scalar() or 0
    
    chat = ChatSession(
        session_id=str(uuid.uuid4()),
        user_id=user_id,
        user_chat_number=max_chat_number + 1,
        title=title,
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)

    if _number_default_chat(chat):
        db.commit()
        db.refresh(chat)

    return chat


def _get_chat_query(db: Session):
    return db.query(ChatSession).options(joinedload(ChatSession.messages))


def get_chat(db: Session, chat_identifier):
    query = _get_chat_query(db)

    if isinstance(chat_identifier, int) or (
        isinstance(chat_identifier, str) and chat_identifier.isdigit()
    ):
        chat_identifier = int(chat_identifier)
        chat = query.filter(ChatSession.id == chat_identifier).first()
    else:
        chat = query.filter(ChatSession.session_id == str(chat_identifier)).first()

    if chat is not None and _number_default_chat(chat):
        db.commit()
        db.refresh(chat)

    return chat


def get_user_chat(db: Session, chat_identifier, user_id: int):
    chat = get_chat(db, chat_identifier)
    return chat if chat is not None and chat.user_id == user_id else None


def _number_default_chats(db: Session, chats: list[ChatSession]):
    changed = False

    for chat in chats:
        if _number_default_chat(chat):
            changed = True

    if changed:
        db.commit()
        for chat in chats:
            db.refresh(chat)


def get_user_chats(db: Session, user_id: int):
    chats = (
        db.query(ChatSession)
        .options(joinedload(ChatSession.messages))
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )

    _number_default_chats(db, chats)

    return chats


def transfer_user_chats(db: Session, source_user_id: int, target_user_id: int) -> int:
    if source_user_id == target_user_id:
        return 0

    target_max_chat_number = db.query(func.max(ChatSession.user_chat_number)).filter(
        ChatSession.user_id == target_user_id
    ).scalar() or 0

    chats = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == source_user_id)
        .order_by(ChatSession.created_at.asc(), ChatSession.id.asc())
        .all()
    )

    for index, chat in enumerate(chats, start=1):
        chat.user_id = target_user_id
        chat.user_chat_number = target_max_chat_number + index

    if chats:
        db.commit()

    return len(chats)


def get_all_chats(db: Session):
    chats = (
        db.query(ChatSession)
        .options(joinedload(ChatSession.messages))
        .order_by(ChatSession.created_at.desc())
        .all()
    )

    _number_default_chats(db, chats)

    return chats


def get_user_chat_count(db: Session, user_id: int):
    return db.query(ChatSession).filter(ChatSession.user_id == user_id).count()


def get_user_message_count(db: Session, user_id: int):
    return (
        db.query(Message)
        .join(ChatSession, Message.chat_session_id == ChatSession.id)
        .filter(ChatSession.user_id == user_id)
        .count()
    )


def delete_chat(db: Session, chat_identifier):
    chat = get_chat(db, chat_identifier)
    if chat is None:
        return False

    db.query(Message).filter(Message.chat_session_id == chat.id).delete(synchronize_session=False)
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
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(message)
    return message
