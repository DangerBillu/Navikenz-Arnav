# Frontend

This folder contains the Vite React application for Navikenz. It owns Auth0 login/signup entry points, guest session behavior, the chat dashboard, static assets, and browser API calls to the FastAPI backend.

## Entry Points

- `index.html` is the Vite HTML shell.
- `src/main.jsx` mounts the React app and Auth0 provider.
- `src/App.jsx` controls authenticated, guest, login, signup, and dashboard flows.

## Scripts

- `npm run dev` starts the local Vite dev server.
- `npm run build` creates the production build in `dist`.
- `npm run lint` runs ESLint.

## Folder Map

- `public/` contains static files served as-is.
- `src/` contains React source code, styles, assets, pages, components, and services.
- `dist/` is generated build output and should not be edited by hand.
