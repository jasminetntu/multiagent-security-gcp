from google.adk.agents import Agent

def handle_request(request: str) -> dict:
    return {
            "status": "success",
            "response": "Acknowledged Compute Engine request."
        }

compute_engine_agent = Agent(
    name="compute_engine_agent",
    model="gemini-2.0-flash",
    description="Specialized agent to answer requests regarding Google Compute Engine.",
    instruction="You are a helpful agent that specializes in answering questions and providing detailed information " 
                "related to Google Compute Engine. If unsure, tell the user it has been acknowledged and nothing else.",
    tools=[handle_request],
)