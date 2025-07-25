from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
import time

from ..searchAgent import search_agent
from cloudsploitFunction.call_cspl import setup_scan

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
        "response": "Successfully waited for 5 seconds for Compute Engine agent."
    }

def scan_vulnerabilities() -> dict:
    return setup_scan("compute")

gce_agent = Agent(
    name="gce_agent",
    model=MODEL,
    description="Answer GCE related questions",
    instruction="""
                You are a helpful agent that specializes in answering questions and providing detailed information related to Google Compute Engine.
                If user says to use wait, call the wait_for_5_seconds.
                If user says to use google search, transfer to the search_agent to perform a google search.
                If user says to scan a vulnerability in their Compute Engine project, call the scan_vulnerabilities.
                    Once the scan is complete, first provide a summary of the top 5 most severe vulnerabilities and how easy
                    they are to fix (easy, medium, hard). Also provide a 3-4 sentence summary on what it is and how to fix it.
                    Follow this format:
                        1. Vulnerability name:
                            - Severity: ...
                            - Ease of fix: ...
                            - Summary: ...
                        2. ...
                        and so on until 5.
                    Then, provide a table format of all the data from the scan. The table should have 4 columns: vulnerability name, 
                    severity, ease of fix, and a 1-2 sentence summary of what the vulnerability is & how to fix it. 
                    If there are 0 vulnerabilities, say "Congrats! Your project has no vulnerabilities."
                Otherwise, provide the answer to the best of your ability.
                """,
    tools=[answer_request,
            wait_5_seconds,
            scan_vulnerabilities,
            AgentTool(search_agent)],
    # sub_agents=[search_agent],
)