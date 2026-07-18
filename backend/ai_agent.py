from dotenv import load_dotenv
from huggingface_hub import login
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
import os
import sys
from datetime import datetime, timezone
from typing import Optional, Tuple
from urllib.parse import urlparse

import requests

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN:
    login(token=HF_TOKEN)
else:
    print("Warning: HF_TOKEN is not set. AI responses may not work.", file=sys.stderr)

endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3.5-9B",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.3,
)

llm = ChatHuggingFace(llm=endpoint)
memory = InMemorySaver()

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@tool
def get_word_count(text: str) -> str:
    """Counts the total number of words in a given piece of text. Use this when asked to count words."""
    word_count = len(text.split())
    return f"The provided text contains exactly {word_count} words."


@tool
def convert_celsius_to_fahrenheit(celsius: float) -> str:
    """Converts a temperature value from Celsius to Fahrenheit."""
    fahrenheit = (celsius * 9 / 5) + 32
    return f"{celsius}°C is equal to {fahrenheit}°F."


def _github_headers() -> dict:
    """Builds request headers for the GitHub REST API, adding auth if GITHUB_TOKEN is set."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def _parse_github_query(query: str) -> Tuple[str, Optional[str]]:
    """
    Extracts (owner, repo) from a GitHub username/org, an 'owner/repo' string,
    or a github.com URL (profile, repo, /tree/, /blob/, .git, or SSH form).
    repo is None when the query only identifies a user or org.
    """
    query = query.strip().strip("<>").rstrip("/")
    if not query:
        raise ValueError("empty query")

    if "gist.github.com" in query:
        raise ValueError("gist links aren't supported, only users, orgs, and repositories")

    if "github.com" in query:
        if query.startswith("git@github.com:"):
            path = query.split("git@github.com:", 1)[1]
        else:
            if not query.startswith("http"):
                query = "https://" + query
            path = urlparse(query).path
        if path.endswith(".git"):
            path = path[:-4]
        parts = [p for p in path.split("/") if p]
        if not parts:
            raise ValueError("no username or repository found in that URL")
        owner, repo = parts[0], (parts[1] if len(parts) > 1 else None)
        return owner, repo

    if "/" in query:
        parts = [p for p in query.split("/") if p]
        if not parts:
            raise ValueError("could not parse that as a user or repository")
        owner, repo = parts[0], (parts[1] if len(parts) > 1 else None)
        return owner, repo

    return query, None


def _rate_limit_message(resp: requests.Response) -> Optional[str]:
    """Returns a friendly message if the response indicates GitHub's rate limit was hit, else None."""
    if resp.status_code in (403, 429) and resp.headers.get("x-ratelimit-remaining") == "0":
        reset_ts = resp.headers.get("x-ratelimit-reset")
        when = ""
        if reset_ts:
            reset_time = datetime.fromtimestamp(int(reset_ts), tz=timezone.utc)
            when = f" It resets at {reset_time.strftime('%H:%M UTC')}."
        return (
            "GitHub API rate limit reached." + when +
            " Set a GITHUB_TOKEN environment variable to raise the limit from 60 to 5,000 requests/hour."
        )
    return None


def _top_starred_repos(owner: str, limit: int = 5):
    """Best-effort fetch of an owner's top non-fork repos by star count. Fails silently to []."""
    try:
        resp = requests.get(
            f"{GITHUB_API}/users/{owner}/repos",
            headers=_github_headers(),
            params={"per_page": 100, "sort": "updated", "type": "owner"},
            timeout=10,
        )
        if not resp.ok:
            return []
        repos = sorted(resp.json(), key=lambda r: r.get("stargazers_count", 0), reverse=True)
        return [
            (r["name"], r.get("stargazers_count", 0), r.get("description") or "No description")
            for r in repos
            if not r.get("fork")
        ][:limit]
    except requests.exceptions.RequestException:
        return []


def _fetch_repo_info(owner: str, repo: str) -> str:
    resp = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}", headers=_github_headers(), timeout=10)

    limit_msg = _rate_limit_message(resp)
    if limit_msg:
        return limit_msg
    if resp.status_code == 404:
        return f"No GitHub repository found at '{owner}/{repo}'."
    if not resp.ok:
        return f"GitHub API returned an error ({resp.status_code}) for '{owner}/{repo}'."

    data = resp.json()
    lines = [
        f"Repository: {data.get('full_name')}",
        f"Description: {data.get('description') or 'No description provided.'}",
        f"URL: {data.get('html_url')}",
        f"Primary language: {data.get('language') or 'Not specified'}",
        f"Stars: {data.get('stargazers_count', 0):,}",
        f"Forks: {data.get('forks_count', 0):,}",
        f"Open issues: {data.get('open_issues_count', 0):,}",
        f"License: {(data.get('license') or {}).get('name', 'None')}",
        f"Default branch: {data.get('default_branch')}",
        f"Last updated: {data.get('updated_at')}",
    ]
    topics = data.get("topics") or []
    if topics:
        lines.append(f"Topics: {', '.join(topics)}")
    if data.get("fork"):
        lines.append("Note: this repository is a fork.")
    if data.get("archived"):
        lines.append("Note: this repository is archived.")

    return "\n".join(lines)


def _fetch_user_info(owner: str) -> str:
    resp = requests.get(f"{GITHUB_API}/users/{owner}", headers=_github_headers(), timeout=10)

    limit_msg = _rate_limit_message(resp)
    if limit_msg:
        return limit_msg
    if resp.status_code == 404:
        return f"No GitHub user or organization found for '{owner}'."
    if not resp.ok:
        return f"GitHub API returned an error ({resp.status_code}) for '{owner}'."

    data = resp.json()
    is_org = data.get("type") == "Organization"
    header = f"{'Organization' if is_org else 'User'}: {data.get('login')}"
    if data.get("name"):
        header += f" ({data['name']})"

    lines = [
        header,
        f"Bio: {data.get('bio') or 'No bio provided.'}",
        f"URL: {data.get('html_url')}",
        f"Public repos: {data.get('public_repos', 0):,}",
    ]
    if not is_org:
        lines.append(f"Followers: {data.get('followers', 0):,}")
        lines.append(f"Following: {data.get('following', 0):,}")
    if data.get("company"):
        lines.append(f"Company: {data['company']}")
    if data.get("location"):
        lines.append(f"Location: {data['location']}")
    if data.get("blog"):
        lines.append(f"Website: {data['blog']}")

    top_repos = _top_starred_repos(owner)
    if top_repos:
        lines.append("Top repositories:")
        lines.extend(f"  - {name} ({stars:,} stars): {desc}" for name, stars, desc in top_repos)

    return "\n".join(lines)


@tool
def github_lookup(query: str) -> str:
    """
    Looks up a GitHub user, organization, or repository and returns key public details.

    Accepts any of:
    - a username or org name, e.g. "torvalds"
    - an "owner/repo" string, e.g. "torvalds/linux"
    - a full GitHub URL, e.g. "https://github.com/torvalds" or
      "https://github.com/torvalds/linux/tree/master"

    Use this whenever the user asks about a GitHub profile, org, or repository,
    or shares a github.com link and wants details like stars, forks, followers,
    bio, description, or primary language. Never make up GitHub stats yourself.
    """
    if not query or not query.strip():
        return "Please provide a GitHub username, 'owner/repo', or a github.com link."

    try:
        owner, repo = _parse_github_query(query)
    except ValueError as exc:
        return f"Could not parse '{query}' as a GitHub user or repository: {exc}"

    try:
        if repo:
            return _fetch_repo_info(owner, repo)
        return _fetch_user_info(owner)
    except requests.exceptions.RequestException as exc:
        return f"Network error while contacting GitHub: {exc}"


system_prompt = """
You are a helpful AI assistant which is trained to answer user queries.
Rules:
- Be concise and accurate.
- If a tool can answer the user's question, always use the appropriate tool. Never make up the result of a tool.
- If no tool is needed, answer normally.
- Remember information shared by the user during the conversation.
Formatting rules:
- Use Markdown.
- Use headings for long answers.
- Use bullet lists when appropriate.
- Use numbered steps for instructions.
- Put code inside fenced code blocks with the correct language.
- Use tables when comparing items.
- Highlight important terms using **bold**.
- Keep answers concise but well structured.
"""

agent = create_react_agent(
    model=llm,
    tools=[get_word_count, convert_celsius_to_fahrenheit, github_lookup],
    prompt=system_prompt,
    checkpointer=memory,
)

config = {"configurable": {"thread_id": "default"}}


def get_assistant_reply(user_input: str, thread_id: str = None) -> str:
    if not user_input:
        return ""

    try:
        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ]
            },
            config={"configurable": {"thread_id": thread_id or "default"}},
        )

        if isinstance(response, dict) and response.get("messages"):
            return response["messages"][-1].content

        return "Sorry, I could not generate a response."
    except Exception as exc:
        return f"Sorry, I could not generate a response: {exc}"


if __name__ == "__main__":
    print("running")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("terminated")
            break

        response = get_assistant_reply(user_input)
        print("\nAssistant:")
        print(response)