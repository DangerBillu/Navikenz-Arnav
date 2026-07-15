from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from huggingface_hub import login
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()
login(token=os.getenv("HF_TOKEN"))

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
You are a helpful AI assistant which is trained to answer to user queries.
Rules:
- Be concise and accurate.
- If a tool can answer the user's question, always use the appropriate tool. Never make up the result of a tool.
- If no tool is needed, answer normally.
- Remember information shared by the user during the conversation.
"""

# system_prompt = """
# You are frech Spider-Man, answer the questions in french .
# Be friendly and use Spider-Man humor occasionally.
# If a tool can answer the question, always use it, never make up tool results.
# """


agent = create_react_agent(
    model=llm,
    tools=[get_word_count, convert_celsius_to_fahrenheit],
    prompt=system_prompt,
    checkpointer=memory,
)

print("running")

config = {"configurable": {"thread_id": "default"}}

while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() in {"exit", "quit"}:
        print("terminated")
        break

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
            config=config,
        )

        print("\nAssistant:")
        print(response["messages"][-1].content)

    except Exception as e:
        print(f"\nError: {e}")