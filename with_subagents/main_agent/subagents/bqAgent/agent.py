from google.adk import Agent
from google.genai import types


MODEL = "gemini-2.5-flash"

bq_agent = Agent(
    name="bq_agent",
    model=MODEL,
    description="Answer BQ related questions",
    instruction="Answer BQ related questions, for now, only say 'Got your question for BQ, will respond soon'",
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
)