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

        # Raise an exception for bad status codes (4xx or 5xx)
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

def setup_scan(product, service_account_key_json):
    """
    Sets up and invokes the scanner with the provided product and key.

    Args:
        product (str): The product or plugin to scan for.
        service_account_key_json (str): The GCP service account key as a JSON string.
    """
    # --- CONFIGURATION ---
    FUNCTION_URL = "https://cloudsploit-scanner-254116077699.us-west1.run.app/"
    
    try:
        print("Found key is in call_cspl ")
        print(service_account_key_json)

        # Load the key from the JSON string into a dictionary
        service_account_key = json.loads(service_account_key_json)

        

        # Define the settings for the scan
        scan_settings = {
            "product": product
        }
        
        # Call the invoker function with the key dictionary
        response = invoke_cloudsploit_scanner(FUNCTION_URL, service_account_key, scan_settings)

        return {
            "status": "success",
            "response": response
        }
        
    except json.JSONDecodeError:
        return {
            "status": "fail",
            "response": "Invalid JSON format for the service account key."
        }
    except Exception as e:
        return {
            "status": "fail",
            "response": f"An unknown error occurred: {e}"
        }

# For local testing
if __name__ == '__main__':
    # --- CONFIGURATION ---
    FUNCTION_URL = "https://cloudsploit-scanner-254116077699.us-west1.run.app/"
    KEY_FILE_PATH = 'key.json'  # The key file is only used for local testing now

    # --- EXECUTION ---
    try:
        # Define the settings for this specific scan
        scan_settings = {
            "plugin": "automaticRestartEnabled"
        }
        
        # Load the service account key from the file into a dictionary
        if not os.path.exists(KEY_FILE_PATH):
            print(f"Error: Key file not found at '{KEY_FILE_PATH}'. Please create it for local testing.")
        else:
            with open(KEY_FILE_PATH, 'r') as f:
                key_dict = json.load(f)
            
            # Call the function which now handles all logic
            results = invoke_cloudsploit_scanner(FUNCTION_URL, key_dict, scan_settings)
            
            if results:
                print("\n--- SCAN RESULTS (JSON) ---")
                # Pretty-print the JSON response
                print(json.dumps(results, indent=2))
        
    except Exception as e:
        # The function now has its own error handling, but we catch any final issues.
        print(f"An error occurred during local testing: {e}")
