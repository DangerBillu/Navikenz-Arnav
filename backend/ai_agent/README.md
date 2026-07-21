# AI Agent

This package builds the LangGraph-powered assistant used by chat services. The package exports `get_assistant_reply` from `__init__.py`, so callers can depend on `from backend.ai_agent import get_assistant_reply` without knowing the internal file layout.

## Files

- `agent.py` creates the agent and exposes the public reply function.
- `llm.py` loads environment variables, logs into Hugging Face when `HF_TOKEN` is present, and configures the chat model.
- `memory.py` owns the in-memory checkpointer.
- `prompt.py` stores the system prompt.
- `tools.py` defines LangChain tools and the tool registry.
- `github_client.py` contains GitHub REST API helpers used by the GitHub lookup tool.
- `ide.py` provides a small manual terminal runner for local testing.

## Notes

- Keep model/provider setup isolated in `llm.py`.
- Add new assistant tools in `tools.py`; place larger external API clients in their own helper modules.
- Keep `agent.py` focused on orchestration and the public response contract.
