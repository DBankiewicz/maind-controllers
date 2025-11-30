import openai
from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def get_response(prompt: str, model: str = "meta-llama/Llama-3.3-70B-Instruct") -> str:
    client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"), 
        base_url="https://llmlab.plgrid.pl/api/v1"
    )
    response =  client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        # input=f"Znajdz tytul maila" # {m}"
    )
    res =  response.choices[0].message.content
    if res is None:
        res = ''
    return res

async def async_get_response(prompt: str, model: str = "meta-llama/Llama-3.3-70B-Instruct") -> str:
    client = AsyncOpenAI(
        api_key=os.getenv("LLM_API_KEY"), 
        base_url="https://llmlab.plgrid.pl/api/v1"
    )
    response =  await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        # input=f"Znajdz tytul maila" # {m}"
    )
    res =  response.choices[0].message.content
    if res is None:
        res = ''
    return res