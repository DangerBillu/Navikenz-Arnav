# Services

This folder contains backend business logic. Services coordinate CRUD helpers, authenticated users, guest limits, AI responses, and API-facing rules.

## Files

- `chat_services.py` owns chat business behavior, including guest chat/message limits, chat lookup, dashboard stats, deletion authorization, and assistant reply creation.

## Guidelines

- Keep routers thin by placing workflow logic here.
- Raise HTTP exceptions here only when they represent business-rule failures.
- Keep direct SQLAlchemy query details in `backend/crud`.
