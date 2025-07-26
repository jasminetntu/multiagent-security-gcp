from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

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

answer_agent = Agent(
    name="answer_agent",
    model=MODEL,
    description="Helpful agent that answers Google Cloud related questions.",
    instruction="""
                You are a helpful agent that specializes in answering questions and providing detailed information related to Google Cloud Platform.
                If the question is within your scope, call answer_request.
                If you are unsure of the answer, call the search_agent to perform a google search.
                """,
    tools=[answer_request,
            AgentTool(search_agent)],
)