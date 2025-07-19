from google.adk.agents import Agent

def handle_request(request: str) -> dict:
    return {
            "status": "success",
            "response": "Acknowledged Cloud SQL request."
        }

cloud_sql_agent = Agent(
    name="cloud_sql_agent",
    model="gemini-2.0-flash",
    description="Specialized agent to answer requests regarding Google Cloud SQL.",
    instruction="You are a helpful agent that specializes in answering questions and providing detailed information " 
                "related to Google Cloud SQL. If unsure, tell the user it has been acknowledged and nothing else.",
    tools=[handle_request],
)