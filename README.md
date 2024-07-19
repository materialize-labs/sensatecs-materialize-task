# Sensatecs Document Extraction

This application provides a web interface for uploading PDF files, extracting text from them using Google Cloud Platform (GCP) Document AI, and analyzing the extracted text using OpenAI's GPT. The results are displayed within the web app built with Streamlit.

## Prerequisites

- **Python 3.10 or higher**
- **Streamlit**
- **Google Cloud SDK**: For interacting with Google Cloud Storage and Document AI.
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

### 3. Set Up Environment Variables and secrects

```bash
GCP_BUCKET_NAME=<your-gcp-bucket-name>
GCP_PROJECT_ID=<your-gcp-project-id>
GCP_PROCESSOR_ID=<your-gcp-processor-id>
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

## Troubleshooting

- **Google Cloud Authentication**: Ensure the Google Cloud credentials file path is correct.
- **Environment Variables**: Verify that the `.env` file is correctly configured.
- **Dependencies**: Ensure all required packages are installed.
- **Errors and Logs**: Check Streamlit logs for any errors or issues.
