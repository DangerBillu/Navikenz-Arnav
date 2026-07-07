from sqlalchemy.orm import Session

from backend.crud import chat_crud, user_crud


def CreateChat(db: Session, user_id: int, title: str):
    if user_crud.get_user(db, user_id) is None:
        return None
    return chat_crud.create_chat(db, user_id, title)


def GetChat(db: Session, chat_id: int):
    return chat_crud.get_chat(db, chat_id)


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


def SendUserMessage(db: Session, chat_id: int, content: str):
    chat = chat_crud.get_chat(db, chat_id)
    if chat is None:
        return None

    return chat_crud.create_message(db, chat_id, content, BuildAssistantReply())


def DeleteChat(db: Session, chat_id: int):
    return chat_crud.delete_chat(db, chat_id)


def BuildAssistantReply():
    return "hi - under development"
