from google.adk import Agent
from google.genai import types


MODEL = "gemini-2.5-flash"

sql_agent = Agent(
    name="sql_agent",
    model=MODEL,
    description="Answer SQL related questions",
    instruction="Answer SQL related questions, for now, only say 'Got your question for SQL, will respond soon'",
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
)