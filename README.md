# Sensatecs Document Extraction

This application provides a web interface for uploading PDF files, extracting text from them using [Google Cloud Platform (GCP) Document AI](https://cloud.google.com/document-ai), and analyzing the extracted text using OpenAI's GPT. The results are displayed within the web app built with Streamlit.

## Prerequisites

- **Python 3.10 or higher**
- **Streamlit**
- **Google Cloud Service Secrets**: For interacting with Google Cloud Storage and Document AI.
- **OpenAI API Key**: For using GPT.

## Installation

### 1. Create a Virtual Environment

For a clean and isolated environment, create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 2. Install Required Packages

Install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables and Secrets

Create a `.env` file in the root directory of your project and add the following environment variables:

```bash
GCP_BUCKET_NAME=<your-gcp-bucket-name>
GCP_PROJECT_ID=<your-gcp-project-id>
GCP_PROCESSOR_ID=<your-gcp-processor-id>
GCP_SERVICE_TYPE=<your-gcp-service-type>
GCP_PRIVATE_KEY_ID=<your-gcp-private-key-id>
GCP_PRIVATE_KEY=<your-gcp-private-key>
GCP_CLIENT_ID=<your-gcp-client-id>
GCP_AUTH_URI=<your-gcp-auth-uri>
GCP_TOKEN_URI=<your-gcp-token-uri>
GCP_AUTH_PROVIDER_X509_CERT_URL=<your-gcp-provider-cert>
GCP_CLIENT_X509_CERT_URL=<your-gcp-client-cert>
GCP_UNIVERSE_DOMAIN=<your-gcp-universe-domain>
GCP_CLIENT_EMAIL=<your-gcp-client-email>
OPENAI_API_KEY=<your-openai-api-key>
```

## How to Run the Application

### 1. Start the Streamlit App

```bash
streamlit run main.py
```

### 2. Upload a PDF File

- Open the web application in your browser (usually at [http://localhost:8501](http://localhost:8501)).
- Use the file uploader to select and upload a PDF file.

### 3. Run the Extraction Process

- Click the "Run Extractor" button to start the text extraction and analysis process.

### 4. View Results

- After processing, the results will be displayed on the web page.

## Code Explanation

### Main Functions

- **`extract_text_batch(file_paths: list[str])`**: Extracts text from the provided PDF file paths using GCP Document AI.
  - **Parameters**:
    - `file_paths` (List of Strings): The paths of the PDF files to process.
  - **Returns**:
    - Extracted text data.

- **`process_text_with_openai(data)`**: Processes the provided JSON data using OpenAI's GPT-4 Turbo model to extract and format specific medical information, and generate a brief summary.
  - **Parameters**:
    - `data` (Dictionary): JSON data containing various medical records and notes.
  - **Returns**:
    - Processed and formatted data as a JSON object with key-value pairs and a summary.

## Main Execution Flow

1. **File Upload**:
   - Upload the PDF file through the Streamlit interface.
   - The file is uploaded to Google Cloud Storage using the `upload_to_bucket` function.

2. **Text Extraction**:
   - The file's path is used to extract text with `extract_text_batch` from Google Cloud Document AI.

3. **Text Analysis**:
   - Process the extracted text using OpenAI GPT with `process_text_with_openai`.

4. **Result Display**:
   - The results are displayed on the Streamlit app using `st.json`.

## Architecture and File Descriptions

### File Structure

- **main.py**: The entry point of the application. It sets up the Streamlit interface and handles file uploads and extraction processes.
- **config.py**: Contains the setup for Google Cloud credentials.
- **bucket.py**: Handles file uploads to Google Cloud Storage.
- **extract.py**: Contains functions for extracting text from PDF files using GCP Document AI.
- **gpt.py**: Contains functions for processing extracted text using OpenAI's GPT.
- **helpers.py**: Utility functions for processing and extracting text from Document AI responses.
- **requirements.txt**: Lists all the Python dependencies required for the project.
- **.env**: Environment variables for configuring the application (not included in the repository, must be created manually).

### How to Use the Files

- **main.py**: Run this file to start the Streamlit application.
- **config.py**: Automatically called by `main.py` to set up Google Cloud credentials.
- **bucket.py**: Used by `main.py` to upload files to Google Cloud Storage.
- **extract.py**: Called by `main.py` to extract text from uploaded PDF files.
- **gpt.py**: Called by `main.py` to process extracted text using OpenAI's GPT.
- **helpers.py**: Provides helper functions used by `extract.py` for text extraction.

## Troubleshooting

- **Environment Variables**: Verify that the `.env` file is correctly configured.
- **Dependencies**: Ensure all required packages are installed.
- **Errors and Logs**: Check Streamlit logs for any errors or issues.