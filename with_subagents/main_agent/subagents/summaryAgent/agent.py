from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

MODEL = "gemini-2.5-flash"

summary_agent = Agent(
    name="summary_agent",
    model=MODEL,
    description="Agent that summarizes and formats the vulnerability scan.",
    instruction="""
                You are a helpful agent that summarizes a .json file containing the results of a vulnerability scan.
                First, provide a summary of the top 5 most severe vulnerabilities and how easy they are to fix (easy, medium, hard). 
                Also provide a 3-4 sentence summary on what it is and how to fix it.
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
                """,
    generate_content_config=types.GenerateContentConfig(
                temperature=0.5,
            ),
            #unsure if this works
)