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
        - Always introduce yourself before any prompt from the user by stating you can help users with a question 
        about a Google Cloud Platform product and also scan vulnerabilities in the user's Google Cloud project.
        - When they respond, understand their query and transfer to one of these agents:
        if it's a general question, send it to the answer_agent to answer the question,
        if it requires a scan, then check if key's value which is {key} is notAvailable, 
                - if it is, then add to your response that {key} is notAvailable then ask the user to send the key in chat to perform a vulnerability scan.
                        - send the key to set_key_agent to set it to the state
                - if {key} is available, then call scanner_agent to run the scan with the available key
        Always send the full request.
        For all else, say "Currently not supported."
        """

SEARCH_AGENT_DESCRIPTION = "Professional agent that performs a Google Search given a request."