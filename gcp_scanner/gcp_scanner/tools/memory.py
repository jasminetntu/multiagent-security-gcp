from gcp_scanner.shared_libraries import constants

from datetime import datetime
import json
import os
from typing import Dict, Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

from dotenv import load_dotenv
import os

load_dotenv()


def _set_initial_states(callback_context: CallbackContext):
    """
    Setting the initial session state given a JSON object of states.

    Args:
        source: A JSON object of states.
        target: The session state object to insert into.
    """

    target = callback_context.state
    target[constants.KEY] = os.getenv("SERVICE_ACCOUNT_KEY")
    target[constants.VULNERABILITIES] = {}

    newState = {
        "key": os.getenv("SERVICE_ACCOUNT_KEY")
    }
    target.update(newState)