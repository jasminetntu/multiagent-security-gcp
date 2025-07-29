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

from .subagents.setKeyAgent import set_key_agent



from .prompt import ROOT_AGENT_INSTRUCTION


root_agent = LlmAgent(
    name="gcp_coordinator",
    model=MODEL,
    description=("""You're hte root agent who will direct to the correct agent. 
s
    If {key} is notAvailable and the user asks for a scan, ask for the key, then call the set_key_agent"
    For any other question, follow the instruction to call the correct agent"""),
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[answer_agent, scanner_agent, set_key_agent],
)





