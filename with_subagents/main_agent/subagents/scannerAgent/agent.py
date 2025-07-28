from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from cloudsploitFunction.call_cspl import setup_scan

MODEL = "gemini-2.5-flash"

from .prompt import SCANNER_PROMPT

def scan_vulnerabilities(product: str) -> dict:
    return setup_scan(product)

scanner_agent = Agent(
    name="scanner_agent",
    model=MODEL,
    description="Agent that performs vulnerability scan.",
    instruction=SCANNER_PROMPT,
    tools=[scan_vulnerabilities],
)