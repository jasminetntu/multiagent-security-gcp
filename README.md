# 🍓🥞 **Strawberry ScanCake**
>*Google Cloud Sprinternship | Break Through Tech Summer 2025*

## Overview
Strawberry ScanCake (SSC) is a microservice, multi-agent AI system designed to streamline security analysis for Technical Account Managers (TAMs). Developed to answer Google Cloud Platform product queries and identify project vulnerabilities, SSC leverages LLMs and the Google Agent Development Kit (ADK) to improve the output readability of a refactored version of the legacy CloudSploit security repository. This automates the manual work of deciphering long, convoluted reports, allowing TAMs to focus on customer needs and ask more detailed follow-up questions about specific vulnerabilities (e.g., severity, ease of fix, and steps to fix).

### Contributors
- Jasmine Tu, Ena Macahiya, Izabella Doser, Vaishnavi Panchal, Anusri Nagarajan, Aman Shrestha

### Relevant Links
- Refactored Cloudsploit Repository: https://github.com/amanshresthaatgoogle/cloudsploit
- Presentation Slides: https://docs.google.com/presentation/d/136oYaZ4lGX4DScbNB0T87cwMVy0qAMPrafPfqPJz57M/edit?usp=sharing

## Quick Start

### Clone and Install Repo
```
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
### Enter 'gcp_scanner' Folder
```
cd gcp_scanner
```
### Run Locally
```
adk web
```
## How It Works
