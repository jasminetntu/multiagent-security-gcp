from google.adk.agents import Agent

def handle_request(request: str) -> dict:
    return {
            "status": "success",
            "response": "Acknowledged Cloud Storage request."
        }

cloud_storage_agent = Agent(
    name="cloud_storage_agent",
    model="gemini-2.0-flash",
    description="Specialized agent to answer requests regarding Google Cloud Storage.",
    instruction="You are a helpful agent that specializes in answering questions and providing detailed information " 
                "related to Google Cloud Storage. If unsure, tell the user it has been acknowledged and nothing else.",
    tools=[handle_request]
)