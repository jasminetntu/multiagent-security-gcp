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

"""answer_agent for providing answers to user queries."""

from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from . import prompt

from ..searchAgent import search_agent

from google.adk.tools.tool_context import ToolContext


MODEL = "gemini-2.5-flash"

def setKey(tool_context: ToolContext, key: dict) -> dict:
    """
    Get the key from user and set key into the state

    Args: key
    Returns: dict with status and response
    """

    # Check the key
    print("Key found is ")
    print(key)
    key['status'] = 200
    tool_context.state["key"] = key
    return {
            "status": "success",
            "response": types.GenerateContentConfig(
                temperature=1,
            )
        }

set_key_agent = Agent(
    name="set_key_agent",
    model=MODEL,
    description="Get the key and call setKey tool to set the key into the state",  # Using description from prompt.py
    instruction="Get the key and call setKey tool to set the key into the state",  # Using instruction from prompt.py
    tools=[
        setKey,
    ],
)