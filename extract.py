import os
import re
import time
import json
import itertools
from typing import Optional, Sequence, List

from google.cloud import storage
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import RetryError

from helpers import extract_lines, extract_blocks, extract_paragraphs, save_extracted_data

gcp_bucket_name=os.getenv('GCP_BUCKET_NAME')
gcp_project_id=os.getenv('GCP_PROJECT_ID')
gcp_processor_id=os.getenv('GCP_PROCESSOR_ID')

def extract_text_batch(
    project_id: str,
    location: str,
    processor_id: str,
    file_paths: list[str],
    mime_type: str,
    save_to_json: bool=False,
    timeout: int = 400,
    field_mask: Optional[str]=None,
) -> dict:
    # Initialize Document AI client with specific client options
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    all_blocks = []
    all_lines = []
    all_paragraphs = []
    all_forms = []
    blobs_to_delete = []

    for file_path in file_paths:
        gcs_document = documentai.GcsDocument(
            gcs_uri=file_path, mime_type=mime_type
        )
        # Load GCS Input URI into a List of document files
        gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
        input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)
        
        gcs_output_config = documentai.DocumentOutputConfig.GcsOutputConfig(
            gcs_uri=f"gs://{gcp_bucket_name}/results/", field_mask=field_mask
        )
        output_config = documentai.DocumentOutputConfig(gcs_output_config=gcs_output_config)

        # Configure the process request
        request = documentai.BatchProcessRequest(
            name=name,
            input_documents=input_config,
            document_output_config=output_config,
        )

        # Process the document
        operation = client.batch_process_documents(request)
        
        try:
            print(f"Waiting for operation {operation.operation.name} to complete...")
            operation.result(timeout=timeout)
        # Catch exception when operation doesn't finish before timeout
        except (RetryError, InternalServerError) as e:
            print(e.message)
            
        metadata = documentai.BatchProcessMetadata(operation.metadata)
        if metadata.state != documentai.BatchProcessMetadata.State.SUCCEEDED:
            raise ValueError(f"Batch Process Failed: {metadata.state_message}")
          
        storage_client = storage.Client()
        
        blocks = []
        lines = []
        paragraphs = []
        forms = []
        
        print("Output files:")
        for process in list(metadata.individual_process_statuses):
          matches = re.match(r"gs://(.*?)/(.*)", process.output_gcs_destination)
          if not matches:
              print(
                  "Could not parse output GCS destination:",
                  process.output_gcs_destination,
              )
              continue

          output_bucket, output_prefix = matches.groups()

          # Get List of Document Objects from the Output Bucket
          output_blobs = storage_client.list_blobs(output_bucket, prefix=output_prefix)

          # Document AI may output multiple JSON files per source file
          for blob in output_blobs:
            blobs_to_delete.append(blob)
            # Document AI should only output JSON files to GCS
            if blob.content_type != "application/json":
                print(
                    f"Skipping non-supported file: {blob.name} - Mimetype: {blob.content_type}"
                )
                continue

            print(f"Fetching {blob.name}")
            document = documentai.Document.from_json(
                blob.download_as_bytes(), ignore_unknown_fields=True
            )

            for page in document.pages:
              print(f"Page {page.page_number}")
              blocks.append({"data": extract_blocks(page.blocks, document.text), "page": page.page_number})
              lines.append({"data": extract_lines(page.lines, document.text), "page": page.page_number})
              paragraphs.append({"data": extract_paragraphs(page.paragraphs, document.text), "page": page.page_number})

        all_blocks.append(blocks)
        all_lines.append(lines)
        all_paragraphs.append(paragraphs)

    # Flatten arrays
    all_blocks = list(itertools.chain.from_iterable(all_blocks))
    all_lines = list(itertools.chain.from_iterable(all_lines))
    all_paragraphs = list(itertools.chain.from_iterable(all_paragraphs))
    
    # Remove Blobs after parsing
    for blob_to_delete in blobs_to_delete: 
        blob_to_delete.delete()
        print(f"File {blob.name} deleted from bucket {gcp_bucket_name}.")
    
    if save_to_json == True:
      save_extracted_data(all_blocks, all_lines, all_paragraphs)

    return {
        "blocks": all_blocks,
        "lines": all_lines,
        "paragraphs": all_paragraphs,
    }

# Test function to store files locally if needed
def extract():
    project_id = gcp_project_id
    processor_id = gcp_processor_id
    location = "us"
    file_paths = [f"gs://{gcp_bucket_name}/1-compressed.pdf"]
    mime_type = "application/pdf"
    field_mask = "text,pages.pageNumber,pages.paragraphs,pages.blocks"

    extract_text_batch(
        project_id,
        location,
        processor_id,
        file_paths,
        mime_type,
        save_to_json=True,
        # field_mask
    )
