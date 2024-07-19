import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

def process_text_with_openai(data):  
    prompt = f"""  
    Extract the following information from the provided JSON, format it as key-value pairs in JSON, and include the source page (marked in JSON as "page") next to each extracted data point:

      - Patient Information (Age, Sex, Race)
      - Diagnosis
      - Medical History
      - Current Medications
      - Prescribed Medications
      - Psychiatric Evaluation
      - Treatment Plan
      - Doctor’s Notes
      - Doctor’s Name
      - Clinical Review (from Detailed Sensatecs Platform section)

    Additionally, provide a brief summary of the medical record based on the extracted information.

    The JSON was parsed from handwriting and may contain incomplete words.
    
    Data: {data}
    """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="gpt-4-turbo",
        response_format={"type": "json_object"},
    )
    json_content = response.choices[0].message.content

    data = json.loads(json_content)
    return data

# with open('extracted_paragraphs.json', 'r') as f:
#     extracted_json_data = json.load(f)
# processed_text = process_text_with_openai(extracted_json_data)
# print("Processed Text:\n", processed_text)