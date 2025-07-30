from google.adk.agents import Agent, callback_context
from google.adk.tools import tool_context, base_tool
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent, LlmAgent
from typing import Optional, Dict, Any
import json

MODEL = "gemini-2.5-flash"

# --- TOOL DEFINITION ---
# This tool is called by the validator when the key is CORRECT.
def exit_key_loop(tool_context: tool_context.ToolContext) -> dict:
    """
    Call this function ONLY when a valid GCP key has been successfully
    processed and stored, signaling the key acquisition loop should end.
    """
    print("--- TOOL CALL: exit_key_loop triggered. Escalating to stop loop. ---")
    # This `escalate` flag is the official way to stop a LoopAgent.
    tool_context.actions.escalate = True
    return {"status": "success", "message": "Loop will now exit."}


# --- AGENT #1: The one that asks for the key ---
# This agent only runs if we don't have a key yet.
def skip_if_key_exists(callback_context: callback_context.CallbackContext) -> str | None:
    """If a key is already in the session, skip this agent entirely."""
    if callback_context.state.get("gcp_key_provided"):
        return "" # An empty string skips the agent.
    return None

key_asker_agent = LlmAgent(
    name="key_asker_agent",
    model=MODEL,
    description="Asks the user to provide their GCP service account key.",
    instruction="""Your only job is to say the following sentence exactly and nothing else: "To perform a security scan, please provide your Google Cloud service account key (key.json content)." """,
    before_agent_callback=skip_if_key_exists
)


# --- AGENT #2: The one that validates the key ---

def validate_and_store_key_in_loop(
    tool: base_tool.BaseTool, args: Dict[str, Any], tool_context: tool_context.ToolContext
) -> Optional[Dict]:
    """
    This callback runs on the LoopAgent. It intercepts the call to exit_key_loop,
    retrieves the user's last message, validates it, and stores it before
    allowing the exit to happen.
    """
    if tool.name != "exit_key_loop":
        return None

    user_text = ""
    # Get the user's input from the session event history.
    if tool_context.session and tool_context.session.events:
        last_event = tool_context.session.events[-1]
        if last_event.author == "user" and last_event.content and last_event.content.parts:
            user_text = last_event.content.parts[0].text
    
    if not user_text:
        return {"status": "fail", "error": "Could not find the user's last message to process."}

    try:
        key_content = json.loads(user_text)
        required_fields = ["type", "project_id", "private_key", "client_email"]
        if all(field in key_content for field in required_fields) and key_content.get("type") == "service_account":
            # SUCCESS! Store the key and set the flag.
            tool_context.state["gcp_key_content"] = key_content
            tool_context.state["gcp_key_provided"] = True
            print("--- LOOP CALLBACK: Key validated and stored. Allowing loop to exit. ---")
            # Let the original `exit_key_loop` run by returning None.
            return None
        else:
            # The JSON is valid, but it's not a service account key.
            # Override the tool call and return an error.
            return {"status": "fail", "error": "The provided JSON is not a valid GCP service account key."}
    except (json.JSONDecodeError, TypeError):
        return {"status": "fail", "error": "The provided text was not in a valid JSON format."}

# This agent receives the user's pasted key and decides whether to exit the loop.
key_validator_agent = LlmAgent(
    name="key_validator_agent",
    model=MODEL,
    description="Validates the user's input as a GCP key and either exits the loop on success or reports an error.",
    instruction=f"""
        You are a key validation assistant. Your input is text provided by a user.
        Analyze the input.
        IF the input looks like a JSON object containing keys like "type", "project_id", and "private_key":
            You MUST call the `exit_key_loop` tool to confirm it is valid and end the process. You MUST also store the key into the session state using the `gcp_key_content` key.
        ELSE (the input is not a valid JSON key):
            You MUST respond with a user-friendly error message explaining that the format was incorrect and ask them to try again. For example: "The provided text does not seem to be a valid JSON key. Please try again."
    """,
    tools=[exit_key_loop],
    before_tool_callback=validate_and_store_key_in_loop
)

# --- AGENT #3: The LoopAgent that manages the process ---
# The LoopAgent manages the key acquisition process.
key_acquirer_loop = LoopAgent(
    name="key_acquirer_loop",
    # The sub_agents run in sequence on each loop iteration.
    sub_agents=[
        key_asker_agent,       # Asks for the key (but only runs if it's missing)
        key_validator_agent,   # Validates the user's response
    ],
)


# def validate_and_store_key(raw_input: str) -> dict:
#     """Validates the raw user input as a GCP key and stores it."""
#     pass

# def run_key_validation(
#     tool: base_tool.BaseTool, args: Dict[str, Any], tool_context: tool_context.ToolContext
# ) -> Optional[Dict]:
#     if tool.name != "validate_and_store_key":
#         return None

#     key_text_to_validate = args.get("raw_input", "")

#     try:
#         key_content = json.loads(key_text_to_validate)
#         required_fields = ["type", "project_id", "private_key", "client_email"]
#         if all(field in key_content for field in required_fields) and key_content.get("type") == "service_account":
#             tool_context.state["gcp_key_content"] = key_content
#             tool_context.state["gcp_key_provided"] = True # This flag stops the loop
#             return {"status": "success", "message": "Key validated and stored."}
#         else:
#             return {"status": "fail", "error": "The JSON is not a valid GCP service account key. It is missing required fields."}
#     except (json.JSONDecodeError, TypeError):
#         return {"status": "fail", "error": "The provided text was not in a valid JSON format."}

# key_agent = Agent(
#     name="key_agent",
#     model=MODEL,
#     description="An agent that repeatedly asks for and validates a user's GCP key.",
#     instruction="""
#         Your single purpose is to acquire a valid GCP service account key from the user.
#         - If this is the first turn, your message MUST be: "To perform a security scan, please provide your Google Cloud service account key (key.json content)."
#         - When the user responds with text, you MUST call the `validate_and_store_key` tool, passing the user's entire, raw response to the `raw_input` parameter.
#         - If the tool call results in a `status` of `fail`, you MUST tell the user the exact `error` message and then ask them to try again. 
#             For example: "That didn't work. The error was: [The provided text was not in a valid JSON format.]. Please paste the correct key content again."
#         - Once the tool call results in a `status` of `success`, your job is done. Your final response should be a simple confirmation like "Your key has been saved."
#     """,
#     tools=[validate_and_store_key],
#     before_tool_callback=run_key_validation
# )