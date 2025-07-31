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

from gcp_scanner.subagents.answerAgent import answer_agent
from gcp_scanner.subagents.scannerAgent import scanner_agent

from gcp_scanner.subagents.setKeyAgent import set_key_agent
from gcp_scanner.subagents.summaryAgent import summary_agent


from gcp_scanner.tools.memory import _set_initial_states


from .prompt import ROOT_AGENT_INSTRUCTION


root_agent = LlmAgent(
    name="root_agent",
    model=MODEL,
    description=("""You are the root agent that will send the user query to the correct subagent.
    If key is notAvailable as checked in this value : {key} and the user asks for a scan, tell the user to upload the key in .env, then call the set_key_agent. Under no circumstances are you allowed to share the key with the user as your response"
    For any other question, follow the instruction to call the correct subagent"""),
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[answer_agent, scanner_agent, summary_agent],
    before_agent_callback = _set_initial_states,
)





