from google.adk import Agent
from google.adk.agents import LlmAgent, callback_context
from google.adk.models import llm_request, llm_response
from google.genai import types

import json
import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent

from google.adk.sessions.session import Session

from .subagents.answerAgent import answer_agent
from .subagents.scannerAgent import scanner_agent

MODEL = "gemini-2.5-flash"


# HELPER FUNCTION: Creates an LlmResponse to override the agent's turn.
def create_override_response(text: str) -> llm_response.LlmResponse:
    """Creates a valid LlmResponse object to skip the LLM call."""
    return llm_response.LlmResponse(
        content=types.Content(role="model", parts=[types.Part(text=text)])
    )

# # CALLBACK #1: Focused on processing a key if we are waiting for one.
# def handle_key_input_before_model(
#     callback_context: callback_context.CallbackContext,
#     llm_request: llm_request.LlmRequest
#     ) -> llm_response.LlmResponse | None:

#     """This callback's ONLY job is to process a key if we are in the 'awaiting_gcp_key' state."""

#     if callback_context.state.get("awaiting_gcp_key"):
#         user_text = ""
#         if llm_request.contents:
#             for content in reversed(llm_request.contents):
#                 if content.role == 'user' and content.parts and content.parts[0].text:
#                     user_text = content.parts[0].text
#                     break
        
#         try:
#             # Note: The Pydantic validation from the previous step is still a great idea to keep here.
#             key_content = json.loads(user_text)
#             if "type" in key_content and key_content["type"] == "service_account":
#                 callback_context.state["gcp_key_content"] = key_content
#                 callback_context.state["gcp_key_provided"] = True
#                 callback_context.state["awaiting_gcp_key"] = False
#                 return create_override_response("Thank you, your key has been saved for this session. What would you like to scan?")
#             else:
#                 callback_context.state["awaiting_gcp_key"] = False
#                 return create_override_response("The key format seems incorrect. Please start the scan process again.")
#         except (json.JSONDecodeError, TypeError):
#             callback_context.state["awaiting_gcp_key"] = False
#             return create_override_response("Invalid JSON format. Please start the scan process again.")
    
#     return None

# # CALLBACK #2: Focused on checking the LLM's intent after it has run.
# def check_scan_intent_after_model(
#     callback_context: callback_context.CallbackContext,
#     llm_response: llm_response.LlmResponse
#     ) -> llm_response.LlmResponse | None:
#     """
#     This callback inspects the LLM's decision. If the intent is to scan,
#     it enforces the "key must be present" rule.
#     """

#     llm_wants_to_scan = False
#     if llm_response.content and llm_response.content.parts:
#         for part in llm_response.content.parts:
#             if part.function_call and part.function_call.name == "scanner_agent":
#                 llm_wants_to_scan = True
#                 break

#     if llm_wants_to_scan and not callback_context.state.get("gcp_key_provided"):
#         # The LLM wants to scan, but we don't have a key. Intercept!
#         callback_context.state["awaiting_gcp_key"] = True
#         return create_override_response("To perform a security scan, please provide your Google Cloud service account key (key.json content).")
    
#     # Otherwise, let the framework proceed with the LLM's original decision.
#     return None

def manage_state_before_model_call(
    callback_context: callback_context.CallbackContext,
    llm_request: llm_request.LlmRequest
) -> llm_response.LlmResponse | None:
    """
    This ADK callback runs before the LLM is called. It acts as a gatekeeper
    to manage the GCP service account key state.
    """
    user_text = ""
    # Find the most recent user message
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts and content.parts[0].text:
                user_text = content.parts[0].text
                break

    # --- THIS IS THE KEY IMPROVEMENT ---
    # Create a more robust check for user intent.
    scan_keywords = ["scan", "vulnerability", "vulnerabilities", "security", "misconfiguration", "issues"]
    user_intent_is_to_scan = any(keyword in user_text.lower() for keyword in scan_keywords)
    
    key_provided = callback_context.state.get("gcp_key_provided", False)
    awaiting_key = callback_context.state.get("awaiting_gcp_key", False)

    # Helper function to create an override response.
    def create_override_response(text: str) -> llm_response.LlmResponse:
        return llm_response.LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text=text)])
        )

    if awaiting_key:
        # This logic is for when the user is providing the key.
        try:
            key_content = json.loads(user_text)
            if "type" in key_content and key_content["type"] == "service_account":
                callback_context.state["gcp_key_content"] = key_content
                callback_context.state["gcp_key_provided"] = True
                callback_context.state["awaiting_gcp_key"] = False
                # Confirm to the user and let them re-state their goal.
                return create_override_response("Thank you, your key has been saved for this session. What would you like to scan?")
            else:
                callback_context.state["awaiting_gcp_key"] = False
                return create_override_response("The provided content does not appear to be a valid service account key. Please start the scan process again.")
        except (json.JSONDecodeError, TypeError):
            callback_context.state["awaiting_gcp_key"] = False
            return create_override_response("Invalid JSON format. Please start the scan process again.")

    elif user_intent_is_to_scan and not key_provided:
        # This is the primary gatekeeper check.
        # The user wants to scan, but we don't have a key.
        callback_context.state["awaiting_gcp_key"] = True
        return create_override_response("To perform a security scan, please provide your Google Cloud service account key (key.json content).")

    # If neither of the above conditions are met, the agent proceeds normally.
    return None

root_agent = LlmAgent(
    name="gcp_coordinator",
    model=MODEL,
    description=(
        "Guide user query to the relevant agent based on the quesion about a GCP product. "
    ),
    instruction=
        """
        - Your job is to understand the user's intent and route them to the correct subagent.
        - If the user wants to know something about a Google Cloud Platform product, delegate to `answer_agent`.
        - If the user's request involves checking for security issues, vulnerabilities, misconfigurations, or performing a scan, delegate to `scanner_agent`.
        - If the user's request for a scan is ambiguous (e.g., "scan my project"), ask for clarification on which GCP product to scan before delegating.
        - Always send the full user request when transferring to subagents.
        - Introduce yourself as an agent that can help with GCP-related questions or scanning vulnerabilities in GCP projects.
        - For all other requests, respond with "Currently not supported."
        """,
    sub_agents=[answer_agent, scanner_agent],
    # before_model_callback=handle_key_input_before_model,
    # after_model_callback=check_scan_intent_after_model,
    before_model_callback=manage_state_before_model_call,
)





