from google.adk import Agent
from google.adk.agents import LlmAgent, callback_context
from google.adk.models import llm_request, llm_response


from dotenv import load_dotenv
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


# def manage_key_state_before_call(callback_context: callback_context.CallbackContext) -> str | None:
#     """
#     This ADK callback runs before the main_agent's LLM is called.
#     It manages the state for the GCP service account key.
    
#     Args:
#         callback_context: A callback_context object provided by the ADK framework.
    
#     Returns:
#         A string to override the agent's response, or None to let it proceed.
#     """
#     user_text = ""
#     if callback_context.prompt and callback_context.prompt.parts:
#         user_text = callback_context.prompt.parts[0].text

def manage_key_state_before_call(
    callback_context: callback_context.CallbackContext,
    llm_request: llm_request.LlmRequest
) -> llm_response.LlmResponse | None:
    """
    This ADK callback runs before the LLM is called for the main_agent.
    It manages the state for the GCP service account key.

    Args:
        callback_context: A context object with access to session state.
        llm_request: The request object about to be sent to the LLM.

    Returns:
        An LlmResponse to override the LLM call, or None to let it proceed.
    """
    user_text = ""

    # The user's input is in the `contents` of the request going to the model.
    if llm_request.contents:
        # Loop backwards through the conversation history.
        for content in reversed(llm_request.contents):
            # Find the first message with the 'user' role.
            if content.role == 'user' and content.parts:
                if content.parts[0].text:
                    user_text = content.parts[0].text
                    break # Stop after finding the most recent user message.
    
    # We only need to intercept if the user is trying to scan.
    is_scan_request = "scan" in user_text.lower() or "vulnerability" in user_text.lower()

    # Access the session state directly from the provided context.
    key_provided = callback_context.state.get("gcp_key_provided", False)
    awaiting_key = callback_context.state.get("awaiting_gcp_key", False)

    
    def create_override_response(text: str) -> llm_response.LlmResponse:
        """Creates a valid LlmResponse object to skip the LLM call."""
        # The constructor takes a `content` object directly.
        return llm_response.LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text=text)],
            )
        )

    if awaiting_key:
        # --- TESTING ---
        print(f"--- DEBUG: RAW INPUT RECEIVED BY PYTHON ---\n{user_text}\n--- END DEBUG ---")

        try:
            key_content = json.loads(user_text)
            if "type" in key_content and key_content["type"] == "service_account":
                callback_context.state["gcp_key_content"] = key_content
                callback_context.state["gcp_key_provided"] = True
                callback_context.state["awaiting_gcp_key"] = False
                # Return None to let the LLM now process the original request.
                return None 
            else:
                callback_context.state["awaiting_gcp_key"] = False
                return create_override_response("The provided content does not appear to be a valid service account key. Please paste the correct JSON content.")
        except json.JSONDecodeError:
            return create_override_response("Invalid JSON format. Please paste the raw content of your key.json file.")
        except Exception as e:
            callback_context.state["awaiting_gcp_key"] = False
            return create_override_response(f"An unexpected error occurred: {e}. Please try scanning again.")

    elif is_scan_request and not key_provided:
        callback_context.state["awaiting_gcp_key"] = True
        # Return an LlmResponse to override the agent and ask for the key.
        return create_override_response("Please provide your Google Cloud service account key (key.json content) for the scan.")

    # If no special state handling is needed, let the agent proceed.
    return None

    # if awaiting_key:
    #     # Case 1: We were waiting for the key, and the user has just provided it.
    #     try:
    #         key_content = json.loads(user_text)
    #         if "type" in key_content and key_content["type"] == "service_account":
    #             # Store the key in the session state. The framework handles saving it.
    #             callback_context.state["gcp_key_content"] = key_content
    #             callback_context.state["gcp_key_provided"] = True
    #             callback_context.state["awaiting_gcp_key"] = False
                
    #             # Let the main agent proceed to delegate to the scanner_agent.
    #             # Returning None tells the framework to continue with the agent's normal execution.
    #             return None 
    #         else:
    #             return "The provided content does not appear to be a valid service account key. Please paste the correct JSON content."
    #     except json.JSONDecodeError:
    #         return "Invalid JSON format. Please paste the raw content of your key.json file."
    #     except Exception as e:
    #         callback_context.state["awaiting_gcp_key"] = False
    #         return f"An unexpected error occurred: {e}. Please try scanning again."

    # elif is_scan_request and not key_provided:
    #     # Case 2: This is a scan request, but we don't have the key yet.
    #     callback_context.state["awaiting_gcp_key"] = True
    #     # By returning a string, we override the agent's normal response.
    #     return "Please provide your Google Cloud service account key (key.json content) for the scan."

    # # Case 3: Not a scan request, or it's a scan request and we already have the key.
    # # Let the agent proceed with its normal logic.
    # return None


root_agent = LlmAgent(
    name="gcp_coordinator",
    model=MODEL,
    description=(
        "Guide user query to the relevant agent based on the quesion about a GCP product. "
    ),
    instruction=
        """    
        - ALWAYS introduce yourself before any prompt from the user by stating you can help users with a question 
        about a Google Cloud Platform product OR with scanning vulnerabilities in the user's Google Cloud project.
        - When they respond, understand their query and transfer to one of these agents:
        If user asks a GCP-related question, transfer to answer_agent.
        If user asks to scan for vulnerabilities, transfer to scanner_agent.
        - If the user asks to scan but does not specify a product, ask them to clarify which Cloud product they want to scan.
        - Always send the full user request when transferring to subagents.
        - For all else, say "Currently not supported."
        """,
    sub_agents=[answer_agent, scanner_agent],
    before_model_callback=manage_key_state_before_call,
)





