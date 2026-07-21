# Pages

This folder contains screen-level React components. Pages coordinate local state, call services, and compose reusable components.

## Files

- `SignInPage.jsx` renders login, signup, and continue-as-guest entry points.
- `DashboardPage.jsx` renders chat history, active messages, sending/deleting chats, and the guest limit modal.

## Guidelines

- Keep page components responsible for workflow state.
- Extract repeated UI into `src/components`.
- Keep backend communication inside `src/services`.
