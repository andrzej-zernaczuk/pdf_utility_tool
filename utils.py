import os
import datetime
from groq import Groq
from openai import OpenAI

api_provider = os.getenv('API_PROVIDER')

if api_provider == 'GROQ':
    client = Groq(
        api_key=os.getenv('GROQ_API_KEY'),
    )
elif api_provider == 'OPENAI':
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        organization=os.getenv('OPENAI_ORG'),
        project=os.getenv('OPENAI_PROJECT'),
    )

def generate_suggested_filename(file_names: list[str]) -> str:
    """Generate a suggested filename for a merged PDF document based on the input file names."""
    suggested_filename = ""
    prompt = f"Based on these PDF file names: {file_names}, respond by suggesting only one concise filename for a merged PDF document. It must be without any spaces, new lines etc.. Write nothing more, just the name of the file without the .pdf extension."

    try:
        response = client.chat.completions.create(
            model=f"{os.getenv(f'{api_provider}_MODEL_ID')}",
            messages=[
                {"role": "user", "content": prompt},
            ],
            # max_completion_tokens=20 #for GPT o1
            max_tokens=20 # for GPT 4o and Groq
        )
        # Extract the suggestion from the response
        # TODO: check if this works for OPENAI
        suggested_filename = response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred while calling the API: {e}")

    # if suggested_filename is empty, generate a default filename
    if not suggested_filename:
        suggested_filename: str = f"merged_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    return suggested_filename