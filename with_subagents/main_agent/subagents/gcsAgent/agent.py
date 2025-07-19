from google.adk import Agent
from google.genai import types


MODEL = "gemini-2.5-flash"

gcs_agent = Agent(
    name="gcs_agent",
    model=MODEL,
    description="Answer GCS related questions",
    instruction="Answer GCS related questions, for now, only say 'Got your question for GCS, will respond soon'",
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
)