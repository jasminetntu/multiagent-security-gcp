from google.adk import Agent
from google.genai import types


MODEL = "gemini-2.5-flash"

gce_agent = Agent(
    name="gce_agent",
    model=MODEL,
    description="Answer GCE related questions",
    instruction="Answer GCE related questions, for now, only say 'Got your question for GCE, will respond soon'",
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
)