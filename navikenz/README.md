# Navikenz

Auth0 handles sign-in and sign-up. The FastAPI service verifies Auth0 access tokens before serving chat data.

## Configuration

Copy the values in the repository's `.env.example` to `.env`. In Auth0, create an **API** and use its Identifier for both `VITE_AUTH0_AUDIENCE` and `AUTH0_AUDIENCE`. Add `http://localhost:5173` to the Auth0 application's Allowed Callback URLs, Allowed Logout URLs, and Allowed Web Origins.

Start the API on port 8000, then start the frontend:

```bash
npm run dev
```
