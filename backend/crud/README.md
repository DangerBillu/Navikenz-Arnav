# CRUD

This folder contains database access helpers. CRUD functions should perform focused reads, writes, updates, and deletes against SQLAlchemy models without owning HTTP concerns or UI-facing behavior.

## Files

- `chat_crud.py` manages chat sessions, messages, chat counts, deletion, and guest-to-user chat transfer.
- `user_crud.py` manages guest users, Auth0 users, profile updates, and user lookup/deletion helpers.

## Guidelines

- Keep transaction boundaries explicit.
- Return model objects or primitive results; raise HTTP errors in routers or services instead.
- Keep business rules in `backend/services` unless the rule is purely about database consistency.
