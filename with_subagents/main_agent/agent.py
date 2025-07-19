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

from .subagents.sqlAgent import sql_agent
from .subagents.bqAgent import bq_agent
from .subagents.gceAgent import gce_agent
from .subagents.gcsAgent import gcs_agent


root_agent = LlmAgent(
    name="gcp_coordinator",
    model=MODEL,
    description=(
        "guide user query to the relevant agent based on the quesion about a gcp product. "
    ),
    instruction=
    """    
    - Let the user know you will help them with a question about a gcp product
    - When they respond, understand their query and transfer to one of 
     gce_agent for gce or compute related question, gcs_agent for gcs related questiosn, bq_agent for bq related questions and sql_agent for sql related questions
     for all else, say "Currently not supported"
     
     """,
 generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
    sub_agents=[gce_agent, gcs_agent, bq_agent, sql_agent],
)





