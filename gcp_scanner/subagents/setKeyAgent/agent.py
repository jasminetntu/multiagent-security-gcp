# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""set_key_agent for getting the key from user and storing in session state."""

from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from . import prompt

from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel, Field
import json


MODEL = "gemini-2.5-flash"

# input schema for the key.json
class KeyInput(BaseModel):
    type: str = Field(description="The type of account.")
    project_id: str = Field(description="The project ID")
    private_key_id: str = Field(description="The private key ID")
    private_key: str = Field(description="The private key")
    client_email: str = Field(description="The client email")
    client_id: str = Field(description="The client ID")
    auth_uri: str = Field(description="The auth URI")
    token_uri: str = Field(description="The token URI")
    auth_provider_x509_cert_url: str = Field(description="The auth provider X.509 cert URL")
    client_x509_cert_url: str = Field(description="The client X.509 cert URL")
    universe_domain: str = Field(description="The universe domain")

# def setKey(tool_context: ToolContext, key: dict) -> dict:
#     """
#     Get the key from user and set key into the state

#     Args: key
#     Returns: dict with status and response
#     """

#     # Check the key
#     print("Key found is ")
#     print(key)
#     key['status'] = 200
#     tool_context.state["key"] = key
#     return {
#             "status": "success",
#             "response": types.GenerateContentConfig(
#                 temperature=1,
#             )
#         }

# set_key_agent = Agent(
#     name="set_key_agent",
#     model=MODEL,
#     description="Get the key and call setKey tool to set the key into the state",  # Using description from prompt.py
#     instruction=
#         """
#         The user will provide a key in JSON format. Get the key and call setKey tool to set the key into the state. 
#         Make sure to set the key as is sent by the user, following the provided input schema. 
#         the fields available are:
#             {"type": "",
#             "project_id": "",
#             "private_key_id": "",
#             "private_key": "",
#             "client_email": "",
#             "client_id": "",
#             "auth_uri": "",
#             "token_uri": "",
#             "auth_provider_x509_cert_url": "",
#             "client_x509_cert_url": "",
#             "universe_domain": ""}
#             The input must be in the exact same order as the input schema.
#             Make sure nothing else is sent to the tool and nothing extra is sent. 
#         """,  # Using instruction from prompt.py
#     tools=[
#         setKey,
#     ],
#     input_schema=KeyInput,
# )


# --- THIS IS THE FIX ---
# Change the function signature to match the fields in KeyInput
def setKey(
    tool_context: ToolContext,
    type: str,
    project_id: str,
    private_key_id: str,
    private_key: str,
    client_email: str,
    client_id: str,
    auth_uri: str,
    token_uri: str,
    auth_provider_x509_cert_url: str,
    client_x509_cert_url: str,
    universe_domain: str,
) -> dict:
    """
    Get the key fields from the user and set the reconstructed key into the state.
    """
    # Reconstruct the key dictionary from the individual arguments
    key_dict = {
        "type": type,
        "project_id": project_id,
        "private_key_id": private_key_id,
        # IMPORTANT: The private key needs its newlines restored. The LLM/JSON
        # parsing process will deliver it with escaped newlines ('\\n').
        "private_key": private_key, #.replace("\\n", "\n"),
        "client_email": client_email,
        "client_id": client_id,
        "auth_uri": auth_uri,
        "token_uri": token_uri,
        "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
        "client_x509_cert_url": client_x509_cert_url,
        "universe_domain": universe_domain,
    }

    print("Key reconstructed and is being set in state.")
    # For debugging, print a sanitized version
    print(json.dumps({k: v for k, v in key_dict.items() if k != 'private_key'}, indent=2))
    
    # Store the complete, correctly formatted dictionary in the state
    tool_context.state["key"] = key_dict
    
    return {"status": "success", "response": "Key has been successfully received and stored."}

# The agent definition remains mostly the same, but you can simplify the prompt
set_key_agent = Agent(
    name="set_key_agent",
    model=MODEL,
    description="Receives a service account key in JSON format and stores it for future use.",
    instruction="""
    The user will provide a service account key in JSON format.
    Your task is to extract all the fields from the provided JSON and call the `setKey` tool with them.
    Ensure every field from the user's JSON is passed to the corresponding argument in the `setKey` tool.
    """,
    tools=[setKey],
    # The input_schema is what enables this mapping, so it's critical to keep it
    input_schema=KeyInput,
)