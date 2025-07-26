from google.adk import Agent
from google.adk.agents import LlmAgent

from dotenv import load_dotenv
from google.genai import types

import os
import logging
import google.cloud.logging

from dotenv import load_dotenv

from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from google.genai import types

MODEL = "gemini-2.5-flash"

from .subagents.answerAgent import answer_agent
from .subagents.scannerAgent import scanner_agent

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
        search_agent to answer the question,
        scanner_agent to perform a vulnerability scan.
        Always send the full request.
        For all else, say "Currently not supported."
        """,
    sub_agents=[answer_agent, scanner_agent],
)





