# Navikenz

Auth0 handles sign-in and sign-up. The FastAPI service validates Auth0 access tokens before serving chat data.

## Configuration

Set `VITE_AUTH0_DOMAIN`, `VITE_AUTH0_CLIENT_ID`, and `AUTH0_DOMAIN` in `.env`. Add `http://localhost:5173` to the Auth0 application's Allowed Callback URLs, Allowed Logout URLs, and Allowed Web Origins.

Start the API on port 8000, then start the frontend:

```bash
npm run dev
```
