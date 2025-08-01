from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from google.adk.tools.tool_context import ToolContext
MODEL = "gemini-2.5-flash"

from . import prompt

summary_agent = Agent(
    name="summary_agent",
    model=MODEL,
    description=prompt.SUMMARY_AGENT_DESCRIPTION, 
    instruction=prompt.SUMMARY_AGENT_INSTRUCTION, 
)