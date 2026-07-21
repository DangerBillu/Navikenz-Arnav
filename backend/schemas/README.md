# Schemas

This folder contains Pydantic models used as API request and response contracts.

## Files

- `chat.py` defines chat creation, message send, chat response, message response, and dashboard response schemas.

## Guidelines

- Keep schemas explicit about API shape.
- Use field constraints for simple validation.
- Do not place database queries or business workflows here.
