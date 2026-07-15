from dotenv import load_dotenv
from huggingface_hub import login
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
import os
import sys

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


system_prompt = """
You are a helpful AI assistant which is trained to answer user queries.
Rules:
- Be concise and accurate.
- If a tool can answer the user's question, always use the appropriate tool. Never make up the result of a tool.
- If no tool is needed, answer normally.
- Remember information shared by the user during the conversation.
"""

agent = create_react_agent(
    model=llm,
    tools=[get_word_count, convert_celsius_to_fahrenheit],
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
