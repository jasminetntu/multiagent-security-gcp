# main_agent/subagents/setKeyAgent/agent.py

import sys
import os
import json
from pydantic import ValidationError
from schemas import GCPServiceAccountKey 

from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from . import prompt

from ..searchAgent import search_agent

from google.adk.tools.tool_context import ToolContext


MODEL = "gemini-2.5-flash"

def setKey(tool_context: ToolContext, key: dict) -> dict:
    """
    Validates and sets the GCP key into the state.

    Args: 
        tool_context: The context for the tool execution.
        key: The input key data. This might be a dict, a string JSON, or 'notAvailable'.

    Returns: 
        A dictionary with status, response configuration, and a message.
    """

    # 1. Handle cases where no key is provided or it's the placeholder 'notAvailable'
    if key is None or key == "notAvailable" or key == "":
        print("No GCP key provided or key is 'notAvailable'. Cannot set key.")
        return {
            "status": "error",
            "response": types.GenerateContentConfig(temperature=0.1), # Config for next LLM turn
            "message": "No GCP service account key was provided. Please provide the key to proceed.",
        }

    # 2. Process provided key (attempt to parse and validate)
    key_dict = None
    try:
        if isinstance(key, str):
            try:
                key_dict = json.loads(key)
            except json.JSONDecodeError:
                print(f"Error: Input 'key' is a string but not valid JSON: {key}")
                return {
                    "status": "error",
                    "response": types.GenerateContentConfig(temperature=0.1),
                    "message": "Invalid JSON format for the key. Please provide valid JSON.",
                }
        elif isinstance(key, dict):
            key_dict = key
        else:
            print(f"Error: Unexpected type for 'key'. Expected dict or JSON string, but got {type(key)}")
            return {
                "status": "error",
                "response": types.GenerateContentConfig(temperature=0.1),
                "message": "Invalid input type for the key. Please provide a JSON object.",
            }

        # Pydantic Validation
        validated_key_data = GCPServiceAccountKey(**key_dict)
        print("GCP Key validated successfully by Pydantic.")

        key_to_store = validated_key_data.model_dump() 

    except ValidationError as e:
        print(f"GCP Key Validation Error: {e}")
        error_message = f"Error: The provided GCP key is invalid. Please ensure all required fields are present and correctly formatted. Specific error: {e}"
        return {
            "status": "error",
            "response": types.GenerateContentConfig(temperature=0.1),
            "message": error_message,
        }
    except Exception as e:
        print(f"An unexpected error occurred during key processing: {e}")
        return {
            "status": "error",
            "response": types.GenerateContentConfig(temperature=0.1),
            "message": f"An unexpected error occurred while processing the key: {e}",
        }

    # If validation passed
    print("Key found and validated:")
    masked_key_to_store = key_to_store.copy()
    if "private_key" in masked_key_to_store:
        masked_key_to_store["private_key"] = "*** (masked)"
    print(masked_key_to_store)

    key_to_store["private_key"] = key_to_store["private_key"].replace("\n","\\n")
    
    tool_context.state["key"] = key_to_store 
    
    return {
        "status": "success",
        "response": types.GenerateContentConfig(temperature=1),
        "message": "Successfully validated and set the GCP service account key.", 
    }

# ... (Rest of your agent definition remains the same) ...
set_key_agent = Agent(
    name="set_key_agent",
    model=MODEL,
    description="Get the key and call setKey tool to set the key into the state",
    instruction="""The user might provide a GCP service account key. If they do, extract it and pass it to the `setKey` tool for validation and storage.
    If the user asks to run scans without providing a key, you should first prompt them to provide the key.
    The expected fields for a GCP key are:
        {"type": "", "project_id": "", "private_key_id": "", "private_key": "", "client_email": "", "client_id": "", "auth_uri": "", "token_uri": "", "auth_provider_x509_cert_url": "", "client_x509_cert_url": "", "universe_domain": ""}
    """,
    tools=[
        setKey,
    ],
)