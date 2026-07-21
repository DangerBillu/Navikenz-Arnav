# Routers

This folder contains FastAPI routers. Routers define HTTP endpoints, request dependencies, response models, and endpoint-specific status handling.

## Files

- `chat.py` exposes chat creation, listing, dashboard stats, detail retrieval, deletion, and message sending.
- `users.py` exposes the health check endpoint.

## Guidelines

- Keep route handlers thin.
- Delegate business logic to `backend/services`.
- Use Pydantic schemas from `backend/schemas` for request and response contracts.
