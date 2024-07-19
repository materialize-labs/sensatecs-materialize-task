import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from bucket import upload_to_bucket
from extract import extract_text_batch
from gpt import process_text_with_openai

gcp_bucket_name=os.getenv('GCP_BUCKET_NAME')
gcp_project_id=os.getenv('GCP_PROJECT_ID')
gcp_processor_id=os.getenv('GCP_PROCESSOR_ID')
path_to_gcp_secret = './secrets/sensatecs-demo-5fef06d9130b.json'

# Set GCP Credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_to_gcp_secret

st.title("Sensatecs Document Extraction")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

def extract_data(file_paths: list[str]):
    project_id = gcp_project_id
    processor_id = gcp_processor_id
    location = "us"
    mime_type = "application/pdf"
    field_mask = "text,pages.pageNumber,pages.paragraphs,pages.blocks"

    return extract_text_batch(
        project_id,
        location,
        processor_id,
        file_paths,
        mime_type,
        save_to_json=True,
        # field_mask
    )

if uploaded_file is not None:
    with st.spinner('Uploading file to Google Cloud Storage...'):
        file_name = uploaded_file.name
        upload_to_bucket(uploaded_file, f"uploads/{file_name}")
        st.success('File uploaded successfully.')

    if st.button('Run Extractor'):
        extracted_data = None

        with st.spinner('Running extraction process...'):
            file_paths = [f"gs://{gcp_bucket_name}/uploads/{file_name}"]
            extracted_data = extract_data(file_paths)

            st.success('Extraction process completed.')
        with st.spinner('Analyzing document...'):
            result = process_text_with_openai(extracted_data["paragraphs"])
                
            st.success('Analyzing process completed.')
                
            st.write("Result:")
            st.json(result)