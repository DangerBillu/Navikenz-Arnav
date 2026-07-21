# Models

This folder contains SQLAlchemy ORM models. Models describe persisted database tables and relationships.

## Files

- `user.py` defines authenticated and guest users.
- `chat_session.py` defines chat sessions and their per-user sequence numbers.
- `message.py` defines stored user prompts and assistant replies.

## Guidelines

- Keep models focused on persistence shape.
- Put business workflows in `backend/services`.
- Put database query helpers in `backend/crud`.
