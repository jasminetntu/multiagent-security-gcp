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

"""search_agent for finding information using google search"""

from google.adk import Agent
from google.adk.tools import google_search
from . import prompt

MODEL = "gemini-2.5-flash"

search_agent = Agent(
    model=MODEL,
    name="search_agent",
    description=prompt.SEARCH_AGENT_DESCRIPTION,  # Using description from prompt.py
    instruction=prompt.SEARCH_AGENT_INSTRUCTION,  # Using instruction from prompt.py
    output_key="search_results_output",          # Consistent output_key
    tools=[google_search],
)