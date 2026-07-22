# Backend

This folder contains the FastAPI application for the chatbot.Auth0 and guest authentication, database access, chat persistence, guest chat limits, and AI-generated replies.

## Entry Points

- `main.py` creates the FastAPI app, configures CORS, initializes database schema checks, and registers routers.
- `config.py` loads environment settings.
- `security.py` gives access to current user from either a bearer token or an anonymous guest id.

## Folder Map

- `ai_agent/` builds the AI assistant.
- `crud/` contains database read/write helpers.
- `database/` owns SQLAlchemy engine setup and schema maintenance.
- `models/` contains SQLAlchemy ORM models.
- `routers/` contains FastAPI routes.
- `schemas/` contains Pydantic request and response models.
- `services/` contains logic that coordinates CRUD, AI, and request rules.
