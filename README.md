# 🍓🥞 **Strawberry ScanCake**
>*Google Cloud Sprinternship | Break Through Tech, Summer 2025*

### Contributors
Jasmine Tu, Ena Macahiya, Izabella Doser, Vaishnavi Panchal, Anusri Nagarajan, Aman Shrestha

## Overview
Strawberry ScanCake (SSC) utilizes micro-service architecture and is a multi-agent AI system designed to streamline security analysis for Technical Account Managers (TAMs). Developed to answer Google Cloud Platform product queries and identify project vulnerabilities, SSC leverages LLMs and the Google Agent Development Kit (ADK) to improve the output readability and simplify the execution of a [refactored version of the legacy CloudSploit security repository](https://github.com/amanshresthaatgoogle/cloudsploit). This automates the manual work of deciphering long, convoluted reports, allowing TAMs to focus on customer needs and ask more detailed follow-up questions about specific vulnerabilities (e.g., severity, ease of fix, and steps to fix) in a specific GCP project.

### Relevant Links
- [Refactored Cloudsploit Repository](https://github.com/amanshresthaatgoogle/cloudsploit)
- [Final Presentation Slides](https://docs.google.com/presentation/d/136oYaZ4lGX4DScbNB0T87cwMVy0qAMPrafPfqPJz57M/edit?usp=sharing)

## Quick Start

### Clone and Install Repo
```
$ git clone https://github.com/jasminetntu/multiagent-security-gcp.git
$ git clone https://github.com/amanshresthaatgoogle/cloudsploit.git
$ cd cloudsploit
$ npm install
```
### Verify Google ADK is Installed
```
pip show google-adk
```
If not, then install Google ADK:
```
pip install google-adk
```
### Navigate to Agent Directory
```
cd ../multiagent-security-gcp/gcp_scanner
```
### Run Agents Locally
```
adk web
```
## How It Works
Strawberry ScanCake consists of two primary components:
1. **Agentic AI System (`gcp_scanner/`)**
   - Built with Google’s Agent Development Kit (ADK).
   - Hosts a web interface (`adk web`) for testing and interacting with the system.
   - Responds to user queries (e.g., “scan my project for compute vulnerabilities”)
   - Sends HTTP POST requests to the deployed Cloud Function with appropriate product and credentials.
   - Processes the vulnerability response and converts it into a natural language explanation.

2. **Refactored CloudSploit Scanner**
   - Hosted as a Google Cloud Function.
   - `main.js` exports a function named `cloudsploitScanner` as the entry point.
   - Accepts a POST request containing:
     - A `serviceAccount` object with the GCP credentials
     - A `settings` object with a `product` key (e.g., Compute)
   - Scans only the specified GCP product (e.g., Compute, IAM, etc.).
   - Filters out all "OK" results and returns a clean JSON of only detected vulnerabilities.

## Deploying CloudSploit to Google Cloud Functions
This deployment will allow CloudSploit to run independently in the cloud and respond to HTTP scan requests.
### Step 1: Setup GCP Environment
```
gcloud config set project [YOUR_PROJECT_ID]
```
Make sure you are authenticated with the correct account.
### Step 2: Deploy the Function
**From within the cloudsploit directory:**
```
gcloud functions deploy cloudsploitScanner \
--runtime nodejs18 \
--trigger-http \
--allow-unauthenticated \
--region=us-west1 \
--memory 1024MB \
--timeout 540s
```
**Ensure that main.js in the cloudsploit directory exports the following:**
```
exports.cloudsploitScanner = async (req, res) => {
  // cloud function handler logic
};
```
**Example Request Payload:**
```
{
  "serviceAccount": {
    "client_email": "...",
    "private_key": "...",
    "project_id": "..."
  },
  "settings": {
    "product": "compute",
    "ignore_ok": true
  }
}
```
The response will be a JSON object containing all detected vulnerabilities grouped by plugin.

## Future Use & Flexibility
- Once deployed the Cloud Function can be called from any client. In our case, we use the agents as the calling tool.
- This is designed to be modular, allowing for both agent side and cloudsploit side to be maintained, edited, and scaled as needed. Components are also replaceable (plugins, output filters, product mapping, etc.)
- Can be redeployed or modified as needs evolve.
- Cloud Function can be shut down to reduce costs post-internship and redeployed on demand.

## License and Attribution
This project is built on a refactored version of [CloudSploit by Aqua Security](https://github.com/aquasecurity/cloudsploit), but has been adapted specifically for Google Cloud and multi-agent systems.
