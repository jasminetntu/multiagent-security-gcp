import json
import requests
import google.auth
from google.oauth2 import service_account
from google.auth.transport import requests as auth_requests
import os
import tempfile


def invoke_cloudsploit_scanner(function_url: str, key_content: dict, settings: dict):
    """
    Makes an authenticated POST request to the deployed CloudSploit scanner function.
    This function accepts key CONTENT, writes it to a temporary file for authentication, and then deletes the file.

    Args:
        function_url (str): The trigger URL of the deployed Cloud Function.
        key_content (dict): The dictionary content of the key.json file.
        settings (dict): A dictionary of settings for the scan.
    """

    temp_key_path = None # Initialize to ensure it's available for the finally block

    try:
        # create temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_key_file:
            json.dump(key_content, tmp_key_file)
            temp_key_path = tmp_key_file.name

        # --- Programmatic Authentication using the temporary file path ---
        print(f"Generating auth token for audience: {function_url}")
        auth_req = auth_requests.Request()
        creds = service_account.IDTokenCredentials.from_service_account_file(
            temp_key_path,
            target_audience=function_url
        )
        creds.refresh(auth_req)
        auth_token = creds.token
        print("Successfully generated auth token from service account key.")
        
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }

        # Load the service account key to be sent in the request body

        payload = {
            "serviceAccount": key_content,
            "settings": settings
        }
        
        print(f"\nSending POST request to: {function_url}")
        print(f"Requesting scan for plugin: {settings.get('product')}")
        
        response = requests.post(function_url, headers=headers, json=payload, timeout=600) # 10 minute timeout
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        # print("\n--- SCAN RESULTS (JSON) ---")
        # # Pretty-print the JSON response
        # print(json.dumps(response.json(), indent=2))

        return response.json()

    except requests.exceptions.RequestException as e:
        print("\n--- REQUEST FAILED ---")
        print(f"An error occurred while making the request: {e}")
        if e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")

        return {
            "status": "fail",
            "response": f"Request failed: {str(e)}"
            }
    except Exception as e:
        print("\n--- SCRIPT ERROR ---")
        print(f"An unexpected error occurred: {e}")
        print("Please ensure the service account has the 'Cloud Functions Invoker' and 'Service Account Token Creator' roles.")
        
        return {
            "status": "fail",
            "response": f"An unexpected script error occurred: {str(e)}"
            }
    finally:
        # --- Clean up the temporary file ---
        # Ensures the temp file is deleted even if errors occur.
        if temp_key_path and os.path.exists(temp_key_path):
            os.remove(temp_key_path)
            print(f"Cleaned up temporary key file: {temp_key_path}")


# --- DEPRECATED FUNCTION ---
# The setup_scan function is no longer needed for the agent flow because
# the hardcoded key path is removed. The tool will call invoke_cloudsploit_scanner directly.
#
# def setup_scan(product):
#     # --- CONFIGURATION ---
#     FUNCTION_URL = "https://cloudsploit-scanner-254116077699.us-west1.run.app/"
    
#     script_dir = os.path.dirname(os.path.abspath(__file__)) # get the directory of script
#     KEY_FILE_PATH = os.path.join(script_dir, 'key.json') # get path of key.json

#     # --- EXECUTION ---
#     try:
#         # Define the settings for scan
#         scan_settings = {
#             "product": product
#         }
        
#         response = invoke_cloudsploit_scanner(FUNCTION_URL, KEY_FILE_PATH, scan_settings)

#         return {
#             "status": "success",
#             "response": response
#         }
        
#     except Exception as e:
#         # The function now has its own error handling, but we catch any final issues.
#         return {
#             "status": "fail",
#             "response": f"unknown error occurred: {e}" #"\nScript failed to complete."
#         }
# ---------

#for local testing
if __name__ == '__main__':
    FUNCTION_URL = "https://cloudsploit-scanner-254116077699.us-west1.run.app/"
    KEY_FILE_PATH = 'key.json' # Local key file for testing

    try:
        # Load the key content from the local file for the test
        with open(KEY_FILE_PATH, 'r') as f:
            test_key_content = json.load(f)

        # Define the settings for this specific scan
        scan_settings = {
            "product": "compute" # Example: scan for Cloud Storage vulnerabilities
        }
        
        # Call the function with the key content
        results = invoke_cloudsploit_scanner(FUNCTION_URL, test_key_content, scan_settings)
        print("\n--- TEST SCAN RESULTS ---")
        print(json.dumps(results, indent=2))
        
    except Exception as e:
        print(f"\nScript failed to complete: {e}")
