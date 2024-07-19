import os
from google.cloud import storage

gcp_bucket_name=os.getenv('GCP_BUCKET_NAME')

def upload_to_bucket(source_file, destination_blob_name):
    """
    Uploads a file-like object to the specified Google Cloud Storage bucket.

    Args:
        source_file (file-like object): The file-like object to be uploaded.
        destination_blob_name (str): The name of the file in the bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcp_bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(source_file)

    print(f"File uploaded to {destination_blob_name}.")
    