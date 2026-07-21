# Navikenz

Navikenz is a full-stack chat application with a FastAPI backend and a Vite React frontend. The backend owns authentication-aware chat persistence, guest limits, and AI response generation. The frontend owns the Auth0 entry flow, guest session handling, and the chat dashboard experience.

## Structure

- `backend/` contains the FastAPI application, database models, CRUD helpers, service logic, routes, schemas, security helpers, and AI agent package.
- `navikenz/` contains the React application, static assets, reusable components, pages, and browser API client.
- `docker-compose.yml` defines local infrastructure.
- `requirements.txt` and `navikenz/package.json` describe backend and frontend dependencies.

## Development Notes

- Keep business rules in `backend/services`.
- Keep database reads/writes in `backend/crud`.
- Keep request/response contracts in `backend/schemas`.
- Keep frontend API calls in `navikenz/src/services`.
- Avoid editing generated folders such as `node_modules`, `dist`, and `__pycache__`.
