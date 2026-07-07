from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def ensure_user_schema():
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("users")}
    if "password_hash" in columns:
        return

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))

def ensure_message_schema():
    inspector = inspect(engine)
    if "messages" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("messages")}
    with engine.begin() as connection:
        if "sent_message" not in columns:
            connection.execute(text("ALTER TABLE messages ADD COLUMN sent_message TEXT"))
        if "received_message" not in columns:
            connection.execute(text("ALTER TABLE messages ADD COLUMN received_message TEXT"))
        connection.execute(
            text(
                "UPDATE messages "
                "SET sent_message = COALESCE(sent_message, content, ''), "
                "received_message = COALESCE(received_message, 'hi - under development') "
                "WHERE sent_message IS NULL OR received_message IS NULL"
            )
        )

        if engine.dialect.name == "postgresql":
            if "sender" in columns:
                connection.execute(text("ALTER TABLE messages ALTER COLUMN sender DROP NOT NULL"))
            if "content" in columns:
                connection.execute(text("ALTER TABLE messages ALTER COLUMN content DROP NOT NULL"))

def check_database_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
