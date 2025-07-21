from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
import time

from ..searchAgent import search_agent

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
    Counts down within terminal.

    Args: none
    Return: dict with status and response
    """
    
    seconds = 5
    while seconds > 0:
        print(f"Waiting for {seconds} seconds...")
        time.sleep(1)
        seconds -= 1

    return {
        "status": "success",
        "response": "Successfully waited for 5 seconds for Cloud Storage agent."
    }

gcs_agent = Agent(
    name="gcs_agent",
    model=MODEL,
    description="Answer GCS related questions",
    instruction="You are a helpful agent that specializes in answering questions and providing detailed information " 
                "related to Google Cloud Storage."
                "If user says to use wait, call the wait_for_5_seconds."
                "If user says to use google search, transfer to the search_agent to perform a google search."
                "Otherwise, provide the answer to the best of your ability.",
    tools=[answer_request,
           wait_5_seconds,
           AgentTool(search_agent)],
)