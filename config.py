import os
import json
import tempfile

# Global variable to keep track of the temporary file path
_temp_file_path = None

def setup_google_cloud_credentials():
    global _temp_file_path
    
    gcp_credentials = {
        "type": os.getenv("GCP_SERVICE_TYPE", "service_account"),
        "project_id": os.getenv("GCP_SERVICE_PROJECT_ID", ""),
        "private_key_id": os.getenv("GCP_PRIVATE_KEY_ID", ""),
        "private_key": os.getenv("GCP_PRIVATE_KEY", "").replace("\\n", "\n"),
        "client_email": os.getenv("GCP_CLIENT_EMAIL", ""),
        "client_id": os.getenv("GCP_CLIENT_ID", ""),
        "auth_uri": os.getenv("GCP_AUTH_URI", ""),
        "token_uri": os.getenv("GCP_TOKEN_URI", ""),
        "auth_provider_x509_cert_url": os.getenv("GCP_AUTH_PROVIDER_X509_CERT_URL", ""),
        "client_x509_cert_url": os.getenv("GCP_CLIENT_X509_CERT_URL", ""),
        "universe_domain": os.getenv("GCP_UNIVERSE_DOMAIN", "googleapis.com"),
    }
    
    # Validate necessary fields
    required_keys = [
        "project_id", "private_key_id", "private_key",
        "client_email", "client_id", "auth_uri",
        "token_uri", "auth_provider_x509_cert_url",
        "client_x509_cert_url"
    ]
    missing_keys = [key for key in required_keys if not gcp_credentials[key]]
    if missing_keys:
        raise ValueError(f"Missing required GCP credentials: {', '.join(missing_keys)}")
    
    # Create a temporary file to store the credentials if it doesn't exist
    if _temp_file_path is None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w') as temp_file:
            json.dump(gcp_credentials, temp_file, indent=4)
            _temp_file_path = temp_file.name
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = _temp_file_path

