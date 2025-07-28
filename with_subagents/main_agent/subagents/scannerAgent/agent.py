from google.adk import Agent
from google.genai import types

from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import tool_context, base_tool

from typing import Optional, Dict, Any

from cloudsploitFunction.call_cspl import invoke_cloudsploit_scanner

MODEL = "gemini-2.5-flash"

# The "dumb" tool signature for the LLM.
def scan_vulnerabilities(product: str) -> dict:
    """Triggers a vulnerability scan for a given GCP product."""
    pass

# The "smart" callback with the real logic.
def run_scan_with_context(
    tool: base_tool.BaseTool, args: Dict[str, Any], tool_context: tool_context.ToolContext
) -> Optional[Dict]:
    if tool.name != "scan_vulnerabilities":
        return None

    product = args.get("product")
    if not product:
        return {"status": "fail", "error": "LLM did not provide a product name."}

    FUNCTION_URL = "https://cloudsploit-scanner-254116077699.us-west1.run.app/"
    gcp_key_content = tool_context.state.get("gcp_key_content")

    if not gcp_key_content:
        return {"status": "fail", "error": "Could not find the GCP key in the session state."}

    response = invoke_cloudsploit_scanner(FUNCTION_URL, gcp_key_content, {"product": product})

    if isinstance(response, dict) and "error" not in response:
        return {"status": "success", "scan_results": response}
    else:
        error_details = response if isinstance(response, dict) else {"details": str(response)}
        return {"status": "fail", "error": error_details}

scanner_agent = Agent(
    name="scanner_agent",
    model=MODEL,
    description="Agent that performs vulnerability scan.",
    instruction="""
                You are a helpful agent that performs a vulnerability scan.
                Your instructions are to identify the specific GCP product the user wants to scan
                from their request, and then call the `scan_vulnerabilities` tool with that product name.
                For example, if the user says "scan cloud storage", you call the tool with product="storage".
                Here is the mapping:
                - api -> "api"
                - bigquery -> "bigquery"
                - bigtable -> "bigtable"
                - cloud load balancing -> "clb"
                - cloud build -> "cloudbuild"
                - cloud functions -> "cloudfunctions"
                - cloud resource manager -> "cloudresourcemanager"
                - composer -> "composer"
                - google compute engine -> "compute"
                - crypto graphic keys -> "cryptographickeys"
                - dataflow -> "dataflow"
                - dataproc -> "dataproc"
                - deployment manager -> "deploymentmanager"
                - dns -> "dns"
                - iam -> "iam"
                - kubernetes -> "kubernetes"
                - logging -> "logging"
                - pubsub -> "pubsub"
                - cloud security -> "security"
                - service usage -> "serviceusage"
                - spanner -> "spanner"
                - cloud sql -> "sql"
                - cloud storage -> "storage"
                - vertex ai -> "vertexai"
                - vpc network -> "vpcnetwork"
                """,
    tools=[scan_vulnerabilities],
    before_tool_callback=run_scan_with_context,
)