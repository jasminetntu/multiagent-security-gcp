from google.adk import Agent
from google.genai import types

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

def google_search(request: str) -> dict:
    """
    Performs a google search.

    Args: request
    Returns: 
    """
    return {
        "status": "success",
        "response": "Google search results."
    }

def wait_5_seconds() -> dict:
    """
    Waits for 5 seconds, then acknowledges when it's finished.
    """
    time.sleep(5)
    return {
        "status": "success",
        "response": "Waited for 5 seconds."
    }

bq_agent = Agent(
    name="bq_agent",
    model=MODEL,
    description="Answer BQ related questions",
    instruction="You are a helpful agent that specializes in answering questions and providing detailed information " 
                "related to Google BigQuery. Answer to the best of your ability. "
                "If unsure, tell the user it has been acknowledged and nothing else.",
    tools=[answer_request,]
           #google_search,
           #wait_5_seconds],
)