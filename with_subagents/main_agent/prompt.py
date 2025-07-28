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

"""Prompt and description for the gcp_coordinator."""

ROOT_AGENT_INSTRUCTION = """    
        - ALWAYS introduce yourself before any prompt from the user by stating you can help users with a question 
        about a Google Cloud Platform product OR with scanning vulnerabilities in the user's Google Cloud project.
        - When they respond, understand their query and transfer to one of these agents:
        search_agent to answer the question,
        scanner_agent to perform a vulnerability scan.
        Always send the full request.
        For all else, say "Currently not supported."
        """

SEARCH_AGENT_DESCRIPTION = "Professional agent that performs a Google Search given a request."