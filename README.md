CURRENTLY: requires the cloudsploit repository to be placed inside the "with_subagents" folder. 

TRYING TO: implement cloud run to separate the 2 repositories

<!-- # Google Sprinternship ADK Agent

This repository contains an agent built with the Google ADK framework. This main_agent calls other subagents, which can answer GCP related questions or scan your project for vulnerabilities. 

## Setup and Installation (ONLY IF USING ENV VARIABLES)

This agent depends on an external vulnerability scanner tool. You must install and configure both projects to run the full application.

**1. Clone Repositories**

First, clone this repository and the required `cloudsploit_refactored_tools` repository into a local directory.

```bash
git clone https://github.com/jasminetntu/GoogleSprinternship.git
git clone https://github.com/amanshresthaatgoogle/cloudsploit_refactored_tools.git
```

**2. Install Dependencies**

<!-- Install the required Python and Node.js packages for each project.

```bash
# Install Python dependencies
cd GoogleSprinternship
pip install -r requirements.txt

# Install Node.js dependencies
cd ../cloudsploit_refactored_tools
npm install
```

**3. Configure the Scanner**

The scanner needs a `config.js` file to know which GCP project to target. Create this file inside the `cloudsploit_refactored_tools` directory.

`cloudsploit_refactored_tools/config.js`:
```javascript
module.exports = {
    google: {
        project_id: 'your-gcp-project-id-goes-here',
    }
};
``` -->

**4. Set Environment Variables**

You must set two environment variables to connect the agent to the scanner and provide Google Cloud authentication.

```bash
# Set this to the absolute path where you cloned the scanner tool
export CLOUDSPLOIT_TOOL_PATH="/path/to/your/cloudsploit_refactored_tools"

# Set this to the absolute path of your GCP service account key file
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/gcp-keyfile.json"
```

**5. Run the Agent**

You are now ready to run the agent.

```bash
cd /path/to/your/GoogleSprinternship/with_subagents

adk web (runs as a web server)
OR
adk run main_agent (runs within terminal)

``` -->
