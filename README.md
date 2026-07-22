# Navikenz
This is a chatbot application with a FastAPI backend and a Vite React frontend. The backend has features like guest chat limits, and AI response generation. The frontend owns the Auth0 entry flow, guest session handling, and the chat dashboard experience.

## Structure

- `backend/` contains the FastAPI application, database models, CRUD helpers, service logic, routes, schemas, security helpers, and AI agent package.
- `navikenz/` contains the React application, static assets, reusable components, pages, and browser API client.
- `docker-compose.yml` defines local infrastructure.
- `requirements.txt` and `navikenz/package.json` describe backend and frontend dependencies.

## Development Notes
- Keep methods/fucntions in `backend/services`.
- Keep database reads and writes in `backend/crud`.
- Keep validations in `backend/schemas`.
- Keep frontend API calls in `navikenz/src/services`.
