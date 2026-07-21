# Services

This folder contains browser-side service modules.

## Files

- `chatApi.js` wraps chat API requests, response parsing, anonymous guest id storage, and auth headers.

## Guidelines

- Keep API endpoint details in this folder.
- Throw clear errors from service functions so pages can show useful UI.
- Preserve `X-Anonymous-User-Id` when authenticated so guest chats can transfer to signed-up users.
