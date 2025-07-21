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
#from .subagents.searchAgent import search_agent

root_agent = LlmAgent(
    name="gcp_coordinator",
    model=MODEL,
    description=(
        "Guide user query to the relevant agent based on the quesion about a GCP product. "
    ),
    instruction=
    """    
    - Let the user know you will help them with a question about a Google Cloud Platform product.
    - When they respond, understand their query and transfer to one of 
     gce_agent for Google Compute Engine or compute-related question,
     gcs_agent for Google Cloud Storage related questiosn,
     bq_agent for BigQuery related questions,
     and sql_agent for Cloud SQL related questions.
     For all else, say "Currently not supported."
     """,
    sub_agents=[gce_agent, gcs_agent, bq_agent, sql_agent],
)





