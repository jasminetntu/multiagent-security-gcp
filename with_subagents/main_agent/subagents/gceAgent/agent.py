from google.adk import Agent
from google.genai import types
import time

from .searchAgent import search_agent

MODEL = "gemini-2.5-flash"

def answer_request(request: str) -> dict:
    """ 
    Answers user's request to best of ability.

    Args: request
    Returns: dict with status and response
    """
    return {
            "status": "success",
            "response": types.GenerateContentConfig(
                temperature=1,
            )
        }

def wait_5_seconds() -> dict:
    """
    Waits for 5 seconds, then acknowledges when it's finished.

    Args: none
    Return: dict with status and response
    """
    time.sleep(5)
    return {
        "status": "success",
        "response": "Waited for 5 seconds."
    }

gce_agent = Agent(
    name="gce_agent",
    model=MODEL,
    description="Answer GCE related questions",
    instruction="You are a helpful agent that specializes in answering questions and providing detailed information " 
                "related to Google Compute Engine. Answer to the best of your ability. "
                "If user says to use google search, transfer to the search_agent to perform a google search.",
    tools=[answer_request],
           #wait_5_seconds],
    sub_agents=[search_agent],
)