import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def process_text_with_openai(data):
    data_str = json.dumps(data)
    prompt = f"""
    You are an advanced AI designed to read and extract information from PDF patient records. You will receive structured JSON data that has been recognized from PDF source documents using OCR technology. The documents contain both typescript and handwritten notes that include various medical details. You need to extract relevant information, including but not limited to:

    - Patient Demographics
    - Diagnosis
    - Medical History
    - Active Medications
    - Treatment Plan
    - Doctor’s Notes

    Additionally, you should also extract the following Clinical Review information:
    - Name
    - Age
    - Sex
    - Payer
    - Height
    - Weight
    - Isolation Status
    - Alert and Oriented x
    - Covid Vaccination Status
    - Recent Covid Test and Result
    - Short term or Long Term Care
    - Diagnosis
    - PMHX (Past Medical History)
    - Expensive/Specialty Medications
    - Equipment Needed
    - Level of Assistance Needed
    - Dialysis Needs
    - List of Medications
    - Tube Feeding
    - Oxygen Needs
    - Trach/Vent
    - Wounds
    - Smoker
    - Drug Abuse
    - Therapy Needs
    - Concerns
    - Status
    - Need to know

    The output should be a structured JSON response containing all the extracted information in a key-value format. Each data point should include the source page number from the PDF where the information was extracted. If there is more than one source page number that the data point came from, include all pages. If there is no source page found, then that means the information could not be found and you should respond with "Not Specified". Additionally, provide a few sentence summary of the medical record based on the information extracted. Here is an example of the desired output format:

    ```json
    {{
        "Patient Demographics": {{
            "Name": {{"value": "John Doe", "source_pages": [1,2]}},
            "Age": {{"value": "44", "source_pages": [3]}},
            ...
        }},
    }}
    ```

    Please extract all relevant information, include the source page number for each data point, and provide a summary of the medical record based on the information extracted. Ensure that the output is a valid JSON object.

    Data: {data_str}
    """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="gpt-4o",
        response_format={"type": "json_object"},
    )
    json_content = response.choices[0].message.content

    data = json.loads(json_content)
    return data

# Example usage:
# with open('extracted_paragraphs.json', 'r') as f:
#     extracted_json_data = json.load(f)
# processed_text = process_text_with_openai(extracted_json_data)
# print("Processed Text:\n", processed_text)
