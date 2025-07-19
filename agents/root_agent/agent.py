from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool #allows us to pass agents in as tools

#import specialized agents' agent.py files as an agent tool
from compute_engine_agent.agent import compute_engine_agent
from cloud_storage_agent.agent import cloud_storage_agent
from cloud_sql_agent.agent import cloud_sql_agent
from bigquery_agent.agent import bigquery_agent

root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description=( #quick description for ease
        "Orchestrator agent for Google Cloud services."
    ),
    instruction=( #instructions for agent
        "You are a helpful Google Assistant agent."
        "Your task is to understand the user's intent and send the user's request to "
        "the correct specialized Google Cloud agent to answer their questions and concerns."
        "Each specialized agent knows all about a specific Google Cloud service, including "
        "Compute Engine, Cloud Storage, Cloud SQL, and BigQuery."
        "For example, if the user mentions VMs, instances, or servers, then use the 'compute_engine_agent' tool."
        "If the user mentions storage, files, or buckets, then use the 'cloud_storage_agent' tool."
        "If the user mentions SQL, then use the 'cloud_sql_agent' tool."
        "If the user mentions BigQuery, then use the 'bigquery_agent' tool."
        "If unsure, ask the user for clarification."
        "Always forward the full user's inquiry."
    ),
    tools=[ #tools agents may need to complete their task
        AgentTool(agent=compute_engine_agent),
        AgentTool(agent=cloud_storage_agent),
        AgentTool(agent=cloud_sql_agent),
        AgentTool(agent=bigquery_agent),
    ],
)
