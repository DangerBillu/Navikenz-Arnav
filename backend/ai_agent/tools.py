from langchain_core.tools import tool
import requests
from backend.ai_agent.github_client import fetch_repo_info, fetch_user_info, parse_github_query


@tool
def get_word_count(text: str) -> str:
    """Counts the total number of words in a given piece of text. Use this when asked to count words."""
    word_count = len(text.split())
    return f"The provided text contains exactly {word_count} words."


@tool
def convert_celsius_to_fahrenheit(celsius: float) -> str:
    """Converts a temperature value from Celsius to Fahrenheit."""
    fahrenheit = (celsius * 9 / 5) + 32
    return f"{celsius} C is equal to {fahrenheit} F."


@tool
def github_lookup(query: str) -> str:
    """
    Looks up a GitHub user, organization, or repository and returns key public details.
    Accepts any of:
    - a username or org name, e.g. "dangerbillu"
    - an "owner/repo" string, e.g. "dangerbillu/catalyx"
    - a full GitHub URL, e.g. "https://github.com/dangerbillu" or
      "https://github.com/dagerbillu/catalyx/tree/master"

    Use this whenever the user asks about a GitHub profile, org, or repository,
    or shares a github.com link and wants details like stars, forks, followers,
    bio, description, or primary language. Never make up GitHub stats yourself.
    """
    if not query or not query.strip():
        return "Please provide a GitHub username, 'owner/repo', or a github link."

    try:
        owner, repo = parse_github_query(query)
    except ValueError as exc:
        return f"Could not parse '{query}' as a GitHub user or repository: {exc}"

    try:
        if repo:
            return fetch_repo_info(owner, repo)
        return fetch_user_info(owner)
    except requests.exceptions.RequestException as exc:
        return f"Network error while contacting GitHub: {exc}"


AGENT_TOOLS = [get_word_count, convert_celsius_to_fahrenheit, github_lookup]
