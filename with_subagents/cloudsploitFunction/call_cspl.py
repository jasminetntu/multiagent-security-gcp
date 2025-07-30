import json
import requests
import google.auth
from google.oauth2 import service_account
from google.auth.transport import requests as auth_requests
import os


def invoke_cloudsploit_scanner(function_url, service_account_key, settings):
    """
    Makes an authenticated POST request to the deployed CloudSploit scanner function.
    This function generates an OIDC token directly from the service account key info.

    Args:
        function_url (str): The trigger URL of the deployed Cloud Function.
        service_account_key (dict): The GCP service account key as a dictionary.
        settings (dict): A dictionary of settings for the scan.
    """
    try:
        # --- Programmatic Authentication ---
        # Instead of reading from a file, we now use the provided key dictionary
        # to generate an identity token for the function's URL (the audience).
        print(f"Generating auth token for audience: {function_url}")
        auth_req = auth_requests.Request()
        
        # Use from_service_account_info to load credentials from a dictionary
        creds = service_account.IDTokenCredentials.from_service_account_info(
            service_account_key,
            target_audience=function_url
        )
        
        creds.refresh(auth_req)
        auth_token = creds.token
        print("Successfully generated auth token from service account key.")
        
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }

        # The service account key is now passed directly in the payload
        payload = {
            "serviceAccount": service_account_key,
            "settings": settings
        }
        
        print(f"\nSending POST request to: {function_url}")
        print(f"Requesting scan for plugin: {settings.get('product') or settings.get('plugin')}")
        
        response = requests.post(function_url, headers=headers, json=payload, timeout=600) # 10 minute timeout

        response.raise_for_status()
        
        return response.json()

    except requests.exceptions.RequestException as e:
        print("\n--- REQUEST FAILED ---")
        print(f"An error occurred while making the request: {e}")
        if e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")
    except Exception as e:
        print("\n--- SCRIPT ERROR ---")
        print(f"An unexpected error occurred: {e}")
        print("Please ensure the service account has the 'Cloud Functions Invoker' and 'Service Account Token Creator' roles.")

def setup_scan(product, service_account_input):
    """
    Sets up and invokes the scanner with the provided product and key.
    This function is now robust and can handle the key as a dictionary OR a JSON string.

    Args:
        product (str): The product or plugin to scan for.
        service_account_input (dict or str): The GCP service account key, either as a
                                             dictionary or a JSON-formatted string.
    """
    # --- CONFIGURATION ---
    FUNCTION_URL = "https://cloudsploit-scanner-254116077699.us-west1.run.app/"
    
    try:
        service_account_key = None
        # Check if the input is a string that needs parsing
        if isinstance(service_account_input, str):
            try:
                # Pre-process the string to replace literal newlines with escaped newlines.
                # The JSON standard requires newlines within strings to be escaped as '\\n'.
                processed_string = service_account_input.replace('\n', '\\n')
                # Attempt to parse the processed string as JSON
                service_account_key = json.loads(processed_string)
            except json.JSONDecodeError:
                return {
                    "status": "fail",
                    "response": "Invalid JSON format for the service account key string. Please ensure it is a valid, single-line JSON string."
                }
        # Check if the input is already a dictionary
        elif isinstance(service_account_input, dict):
            service_account_key = service_account_input
        else:
            # Handle cases where the input is neither a string nor a dictionary
            return {
                "status": "fail",
                "response": f"Unsupported type for service account key: {type(service_account_input).__name__}. Must be a dictionary or a JSON string."
            }

        # --- Post-Processing Validation ---
        # Ensure we ended up with a dictionary after potential parsing
        if not isinstance(service_account_key, dict):
             return {
                "status": "fail",
                "response": "Processed service account key is not a dictionary. This can happen if the input string is a JSON literal (e.g., \"'value'\") instead of a JSON object."
            }

        # --- Key Content Validation ---
        # Check for essential keys to ensure it's a valid service account key
        required_keys = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        if not all(key in service_account_key for key in required_keys) or service_account_key.get('type') != 'service_account':
            return {
                "status": "fail",
                "response": "Invalid service account key format. The dictionary is missing required fields or the 'type' is not 'service_account'."
            }

        # Define the settings for the scan
        scan_settings = {
            "product": product,
            "ignore_ok" : 'true'
        }
        
        # Call the invoker function with the key dictionary
        response = invoke_cloudsploit_scanner(FUNCTION_URL, service_account_key, scan_settings)

        if isinstance(response, dict):
            transformed_vulnerabilities_list = [
                {vulnerability_name: details_list}
                for vulnerability_name, details_list in response.items()
            ]
        else: # response isn't a dict
            print(f"Warning: Unexpected format for scanner response: {type(response).__name__}. Expected a dictionary.")
            transformed_vulnerabilities_list = []

        # Return the final, desired structure
        return {
            product: transformed_vulnerabilities_list
        }

        # return {
        #     product : response
        # }
        
    except Exception as e:
        print("Exception is ")
        print(e)
        return {
            "status": "fail",
            "response": f"An unknown error occurred: {e}"
        }

