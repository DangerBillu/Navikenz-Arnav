# Database

This folder owns SQLAlchemy database setup and schema maintenance.

## Files

- `connection.py` defines the engine, session factory, declarative base, database dependency, connection checks, schema compatibility helpers, and guest chat count synchronization.

## Guidelines

- Use `get_db` as the FastAPI dependency for request-scoped sessions.
- Keep schema migration compatibility helpers idempotent.
- Avoid destructive startup behavior in production paths.
