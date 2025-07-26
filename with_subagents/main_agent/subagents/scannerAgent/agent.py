from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from cloudsploitFunction.call_cspl import invoke_cloudsploit_scanner
from google.adk.tools import tool_context

MODEL = "gemini-2.5-flash"

def scan_vulnerabilities(product: str, context: tool_context.ToolContext) -> dict:
    """
    This tool performs the vulnerability scan.
    The ADK framework automatically provides the 'product' from the LLM's call
    and the 'context' object containing the session state.
    """
    FUNCTION_URL = "https://cloudsploit-scanner-254116077699.us-west1.run.app/"
    gcp_key_content = context.state.get("gcp_key_content")

    if not gcp_key_content:
        # This is a safeguard. If the key is somehow missing, return an error.
        return {
            "status": "fail",
            "response": "Could not find the GCP key in the session state. Please ask the user to start the scan process again."
        }

    response = invoke_cloudsploit_scanner(FUNCTION_URL, gcp_key_content, {"product": product})

    if isinstance(response, dict) and "error" not in response:
        # Successful scan
        return {
            "status": "success", 
            "response": response
        }
    else:
        # Scan failed or returned an error
        error_details = response if isinstance(response, dict) else {"details": str(response)}
        return {
            "status": "fail", 
            "response": error_details}

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
)