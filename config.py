import os
import json
import tempfile

# Global variable to keep track of the temporary file path
_temp_file_path = None

def setup_google_cloud_credentials(gcp_service_key: str):
    global _temp_file_path
    
    if not gcp_service_key:
        raise ValueError("The GCP_SERVICE_KEY environment variable is not set.")
    
    try:
        gcp_service_key_dict = json.loads(gcp_service_key)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON format in GCP_SERVICE_KEY environment variable.") from e

    # If a temp file already exists, skip creation
    if _temp_file_path is None:
        print("Creating a new temporary file..")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
            temp_file.write(gcp_service_key.encode('utf-8'))
            _temp_file_path = temp_file.name
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = _temp_file_path