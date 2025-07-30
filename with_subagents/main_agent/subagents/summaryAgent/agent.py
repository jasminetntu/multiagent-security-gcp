from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from google.adk.tools.tool_context import ToolContext
from colorama import Fore

MODEL = "gemini-2.5-flash"

from . import prompt

# def get_vulnerabilities(tool_context: ToolContext, product: str) -> dict:
#     print(Fore.GREEN + "this is the vuln list " + str(tool_context.state['vulnerabilities']) + Fore.RESET)
#     return tool_context.state['vulnerabilities'] 

summary_agent = Agent(
    name="summary_agent",
    model=MODEL,
    description=prompt.SUMMARY_AGENT_DESCRIPTION, 
    instruction=prompt.SUMMARY_AGENT_INSTRUCTION, 
    output_key="final_answer_output",             # Added output_key for session state
    # tools = [
    #     get_vulnerabilities
    # ]
)