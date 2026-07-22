# Routers

This folder contains FastAPI routes. Routers define HTTP endpoints, request dependencies, response models, and endpoint-specific status handling.

## Files

- `chat.py` - this file has functions like chat creation, listing, dashboard stats, detail retrieval, deletion, and message sending.
- `users.py` - this file checks the connection/health of the database.

## Guidelines

- Write logic/methods in `backend/services`.
- Use Pydantic schemas from `backend/schemas` for request and response validation/sctructure.
