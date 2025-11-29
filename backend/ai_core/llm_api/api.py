from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_response(prompt: str, model: str = "meta-llama/Llama-3.3-70B-Instruct"):
    client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"), 
        base_url="https://llmlab.plgrid.pl/api/v1"
    )
    response =  client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        # input=f"Znajdz tytul maila" # {m}"
    )

    return response.choices[0].message.content
