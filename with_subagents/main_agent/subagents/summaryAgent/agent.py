from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

MODEL = "gemini-2.5-flash"

from .prompt import SUMMARY_PROMPT

summary_agent = Agent(
    name="summary_agent",
    model=MODEL,
    description="Agent that summarizes and formats the vulnerability scan.",
    instruction=SUMMARY_PROMPT,
    generate_content_config=types.GenerateContentConfig(
                temperature=0.5,
            ),
            #unsure if this works
)