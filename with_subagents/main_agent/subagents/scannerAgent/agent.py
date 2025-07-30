from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from cloudsploitFunction.call_cspl import setup_scan

from google.adk.tools.tool_context import ToolContext

MODEL = "gemini-2.5-flash"

from .prompt import SCANNER_PROMPT

def scan_vulnerabilities(tool_context: ToolContext, product: str) -> dict:
    obtained_key = tool_context.state['key']
    vulnerabilities =  setup_scan(product, obtained_key)
    tool_context.state['vulnerabilities'] = vulnerabilities
    return vulnerabilities

scanner_agent = Agent(
    name="scanner_agent",
    model=MODEL,
    description="Agent that performs vulnerability scan.",
    instruction=SCANNER_PROMPT,
    tools=[scan_vulnerabilities],
)