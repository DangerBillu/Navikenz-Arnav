# Backend

This folder contains the FastAPI application for Navikenz. It handles HTTP routing, Auth0 and guest authentication, database access, chat persistence, guest chat limits, and AI-generated replies.

## Entry Points

- `main.py` creates the FastAPI app, configures CORS, initializes database schema checks, and registers routers.
- `config.py` loads environment-backed settings.
- `security.py` resolves the current user from either a bearer token or an anonymous guest id.

## Folder Map

- `ai_agent/` builds and exposes the AI assistant.
- `crud/` contains database read/write helpers.
- `database/` owns SQLAlchemy engine/session setup and schema maintenance.
- `models/` contains SQLAlchemy ORM models.
- `routers/` contains FastAPI route handlers.
- `schemas/` contains Pydantic request and response models.
- `services/` contains business logic that coordinates CRUD, AI, and request rules.
