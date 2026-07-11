from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def _has_foreign_key(inspector, table_name: str, constrained_columns: list[str], referred_table: str):
    expected_columns = set(constrained_columns)
    for foreign_key in inspector.get_foreign_keys(table_name):
        if (
            set(foreign_key.get("constrained_columns", [])) == expected_columns
            and foreign_key.get("referred_table") == referred_table
        ):
            return True
    return False


def _has_index(inspector, table_name: str, index_name: str):
    return any(index["name"] == index_name for index in inspector.get_indexes(table_name))


def ensure_user_schema():
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("users")}
    with engine.begin() as connection:
        if "name" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN name VARCHAR(100)"))
            connection.execute(text("UPDATE users SET name = COALESCE(name, 'Navikenz user')"))
        if "email" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR(100)"))
            connection.execute(text("UPDATE users SET email = COALESCE(email, 'missing-email@auth0.local')"))
        if "phone" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN phone VARCHAR(20)"))
        if "age" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN age INTEGER"))
        if "password_hash" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
        if "auth0_subject" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN auth0_subject VARCHAR(255)"))
        if not _has_index(inspector, "users", "ix_users_auth0_subject"):
            connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_auth0_subject ON users (auth0_subject)"))

        if engine.dialect.name == "postgresql":
            for column in ("phone", "age", "password_hash", "auth0_subject"):
                if column in columns:
                    connection.execute(text(f"ALTER TABLE users ALTER COLUMN {column} DROP NOT NULL"))

def ensure_chat_schema():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    if "chat_sessions" not in table_names:
        return

    columns = {column["name"] for column in inspector.get_columns("chat_sessions")}
    with engine.begin() as connection:
        if not _has_index(inspector, "chat_sessions", "ix_chat_sessions_user_created"):
            connection.execute(
                text("CREATE INDEX IF NOT EXISTS ix_chat_sessions_user_created ON chat_sessions (user_id, created_at)")
            )

        # Add user_chat_number column if it doesn't exist
        if "user_chat_number" not in columns:
            if engine.dialect.name == "sqlite":
                # For SQLite, calculate the chat number for each user based on creation order
                connection.execute(text("""
                    ALTER TABLE chat_sessions ADD COLUMN user_chat_number INTEGER DEFAULT 1
                """))
                # Update existing chats with their per-user sequence number
                connection.execute(text("""
                    WITH numbered_chats AS (
                        SELECT id, user_id, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) as chat_num
                        FROM chat_sessions
                    )
                    UPDATE chat_sessions SET user_chat_number = (
                        SELECT chat_num FROM numbered_chats WHERE numbered_chats.id = chat_sessions.id
                    )
                """))
            else:
                # For PostgreSQL
                connection.execute(text("""
                    ALTER TABLE chat_sessions ADD COLUMN user_chat_number INTEGER DEFAULT 1
                """))
                connection.execute(text("""
                    WITH numbered_chats AS (
                        SELECT id, user_id, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) as chat_num
                        FROM chat_sessions
                    )
                    UPDATE chat_sessions SET user_chat_number = numbered_chats.chat_num
                    FROM numbered_chats WHERE numbered_chats.id = chat_sessions.id
                """))

        if engine.dialect.name == "postgresql" and "users" in table_names:
            connection.execute(
                text(
                    "DELETE FROM chat_sessions "
                    "WHERE user_id IS NULL OR NOT EXISTS ("
                    "SELECT 1 FROM users WHERE users.id = chat_sessions.user_id"
                    ")"
                )
            )
            if not _has_foreign_key(inspector, "chat_sessions", ["user_id"], "users"):
                connection.execute(
                    text(
                        "ALTER TABLE chat_sessions "
                        "ADD CONSTRAINT fk_chat_sessions_user_id "
                        "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE"
                    )
                )

def ensure_message_schema():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    if "messages" not in table_names:
        return

    columns = {column["name"] for column in inspector.get_columns("messages")}
    with engine.begin() as connection:
        if "sent_message" not in columns:
            connection.execute(text("ALTER TABLE messages ADD COLUMN sent_message TEXT"))
        if "received_message" not in columns:
            connection.execute(text("ALTER TABLE messages ADD COLUMN received_message TEXT"))
        sent_fallback = "content" if "content" in columns else "''"
        connection.execute(
            text(
                "UPDATE messages "
                f"SET sent_message = COALESCE(sent_message, {sent_fallback}, ''), "
                "received_message = COALESCE(received_message, 'hi - under development') "
                "WHERE sent_message IS NULL OR received_message IS NULL"
            )
        )

        if engine.dialect.name == "postgresql":
            if "sender" in columns:
                connection.execute(text("ALTER TABLE messages ALTER COLUMN sender DROP NOT NULL"))
            if "content" in columns:
                connection.execute(text("ALTER TABLE messages ALTER COLUMN content DROP NOT NULL"))
            connection.execute(text("ALTER TABLE messages ALTER COLUMN sent_message SET NOT NULL"))
            connection.execute(text("ALTER TABLE messages ALTER COLUMN received_message SET NOT NULL"))

            if "chat_sessions" in table_names:
                connection.execute(
                    text(
                        "DELETE FROM messages "
                        "WHERE chat_session_id IS NULL OR NOT EXISTS ("
                        "SELECT 1 FROM chat_sessions WHERE chat_sessions.id = messages.chat_session_id"
                        ")"
                    )
                )
                if not _has_foreign_key(inspector, "messages", ["chat_session_id"], "chat_sessions"):
                    connection.execute(
                        text(
                            "ALTER TABLE messages "
                            "ADD CONSTRAINT fk_messages_chat_session_id "
                            "FOREIGN KEY (chat_session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE"
                        )
                    )

        if not _has_index(inspector, "messages", "ix_messages_chat_created"):
            connection.execute(
                text("CREATE INDEX IF NOT EXISTS ix_messages_chat_created ON messages (chat_session_id, created_at)")
            )

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
