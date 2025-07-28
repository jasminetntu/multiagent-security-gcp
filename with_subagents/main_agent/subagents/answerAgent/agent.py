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

MODEL = "gemini-2.5-flash"

def answer_request(request: str) -> dict:
    """
    Answers user's request to best of ability.

    Args: request
    Returns: dict with status and response
    """
    return {
            "status": "success",
            "response": types.GenerateContentConfig(
                temperature=1,
            )
        }

answer_agent = Agent(
    name="answer_agent",
    model=MODEL,
    description=prompt.ANSWER_AGENT_DESCRIPTION,  # Using description from prompt.py
    instruction=prompt.ANSWER_AGENT_INSTRUCTION,  # Using instruction from prompt.py
    output_key="final_answer_output",             # Added output_key for session state
    tools=[
        answer_request,
        AgentTool(search_agent) # This allows answer_agent to call search_agent
    ],
)