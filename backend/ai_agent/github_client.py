from datetime import datetime, timezone
import os
from typing import Optional, Tuple
from urllib.parse import urlparse
import requests

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def github_headers() -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def parse_github_query(query: str) -> Tuple[str, Optional[str]]:
    query = query.strip().strip("<>").rstrip("/")
    if not query:
        raise ValueError("empty query")

    if "gist.github.com" in query:
        raise ValueError("gist links are not supported, only users, orgs, and repositories")

    if "github.com" in query:
        if query.startswith("git@github.com:"):
            path = query.split("git@github.com:", 1)[1]
        else:
            if not query.startswith("http"):
                query = "https://" + query
            path = urlparse(query).path

        if path.endswith(".git"):
            path = path[:-4]

        parts = [part for part in path.split("/") if part]
        if not parts:
            raise ValueError("no username or repository found in that URL")

        owner = parts[0]
        repo = parts[1] if len(parts) > 1 else None
        return owner, repo

    if "/" in query:
        parts = [part for part in query.split("/") if part]
        if not parts:
            raise ValueError("could not parse that as a user or repository")

        owner = parts[0]
        repo = parts[1] if len(parts) > 1 else None
        return owner, repo

    return query, None


def rate_limit_message(response: requests.Response) -> Optional[str]:
    if response.status_code not in (403, 429):
        return None

    if response.headers.get("x-ratelimit-remaining") != "0":
        return None

    reset_at = response.headers.get("x-ratelimit-reset")
    reset_message = ""
    if reset_at:
        reset_time = datetime.fromtimestamp(int(reset_at), tz=timezone.utc)
        reset_message = f" It resets at {reset_time.strftime('%H:%M UTC')}."

    return (
        "GitHub API rate limit reached."
        + reset_message
        + " Set a GITHUB_TOKEN environment variable to raise the limit from 60 to 5,000 requests/hour."
    )


def fetch_top_starred_repos(owner: str, limit: int = 5):
    try:
        response = requests.get(
            f"{GITHUB_API}/users/{owner}/repos",
            headers=github_headers(),
            params={"per_page": 100, "sort": "updated", "type": "owner"},
            timeout=10,
        )
        if not response.ok:
            return []

        repos = sorted(response.json(), key=lambda repo: repo.get("stargazers_count", 0), reverse=True)
        return [
            (repo["name"], repo.get("stargazers_count", 0), repo.get("description") or "No description")
            for repo in repos
            if not repo.get("fork")
        ][:limit]
    except requests.exceptions.RequestException:
        return []


def fetch_repo_info(owner: str, repo: str) -> str:
    response = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}", headers=github_headers(), timeout=10)

    limit_message = rate_limit_message(response)
    if limit_message:
        return limit_message
    if response.status_code == 404:
        return f"No GitHub repository found at '{owner}/{repo}'."
    if not response.ok:
        return f"GitHub API returned an error ({response.status_code}) for '{owner}/{repo}'."

    data = response.json()
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


def fetch_user_info(owner: str) -> str:
    response = requests.get(f"{GITHUB_API}/users/{owner}", headers=github_headers(), timeout=10)

    limit_message = rate_limit_message(response)
    if limit_message:
        return limit_message
    if response.status_code == 404:
        return f"No GitHub user or organization found for '{owner}'."
    if not response.ok:
        return f"GitHub API returned an error ({response.status_code}) for '{owner}'."

    data = response.json()
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

    top_repos = fetch_top_starred_repos(owner)
    if top_repos:
        lines.append("Top repositories:")
        lines.extend(f"  - {name} ({stars:,} stars): {description}" for name, stars, description in top_repos)

    return "\n".join(lines)
