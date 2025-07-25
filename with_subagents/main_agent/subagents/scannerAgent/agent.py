from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from cloudsploitFunction.call_cspl import setup_scan

MODEL = "gemini-2.5-flash"

def scan_vulnerabilities(product: str) -> dict:
    return setup_scan(product)

scanner_agent = Agent(
    name="scanner_agent",
    model=MODEL,
    description="Agent that performs vulnerability scan.",
    instruction="""
                You are a helpful agent that performs a vulnerability scan.
                If user asks to scan api vulnerabilities/projects, pass "api" into scan_vulnerabilities.
                If user asks to scan bigquery vulnerabilities/projects, pass "bigquery" into scan_vulnerabilities.
                If user asks to scan bigtable vulnerabilities/projects, pass "bigtable" into scan_vulnerabilities.
                If user asks to scan cloud load balancing vulnerabilities/projects, pass "clb" into scan_vulnerabilities.
                If user asks to scan cloud build vulnerabilities/projects, pass "cloudbuild" into scan_vulnerabilities.
                If user asks to scan cloud function vulnerabilities/projects, pass "cloudfunctions" into scan_vulnerabilities.
                If user asks to scan cloud resource manager vulnerabilities/projects, pass "cloudresourcemanager" into scan_vulnerabilities.
                If user asks to scan composer vulnerabilities/projects, pass "composer" into scan_vulnerabilities.
                If user asks to scan google compute engine vulnerabilities/projects, pass "compute" into scan_vulnerabilities.
                If user asks to scan crypto graphic keys vulnerabilities/projects, pass "cryptographickeys" into scan_vulnerabilities.
                If user asks to scan dataflow vulnerabilities/projects, pass "dataflow" into scan_vulnerabilities.
                If user asks to scan dataproc vulnerabilities/projects, pass "dataproc" into scan_vulnerabilities.
                If user asks to scan deployment manager vulnerabilities/projects, pass "deploymentmanager" into scan_vulnerabilities.
                If user asks to scan dns vulnerabilities/projects, pass "dns" into scan_vulnerabilities.
                If user asks to scan iam vulnerabilities/projects, pass "iam" into scan_vulnerabilities.
                If user asks to scan kubernetes vulnerabilities/projects, pass "kubernetes" into scan_vulnerabilities.
                If user asks to scan logging vulnerabilities/projects, pass "logging" into scan_vulnerabilities.
                If user asks to scan pubsub vulnerabilities/projects, pass "pubsub" into scan_vulnerabilities.
                If user asks to scan cloud security vulnerabilities/projects, pass "security" into scan_vulnerabilities.
                If user asks to scan service usage vulnerabilities/projects, pass "serviceusage" into scan_vulnerabilities.
                If user asks to scan spanner vulnerabilities/projects, pass "spanner" into scan_vulnerabilities.
                If user asks to scan cloud sql vulnerabilities/projects, pass "sql" into scan_vulnerabilities.
                If user asks to scan cloud storage vulnerabilities/projects, pass "storage" into scan_vulnerabilities.
                If user asks to scan vertex ai vulnerabilities/projects, pass "vertexai" into scan_vulnerabilities.
                If user asks to scan vpc network vulnerabilities/projects, pass "vpcnetwork" into scan_vulnerabilities.
                """,
    tools=[scan_vulnerabilities],
)