import pysqlite3
import sys

# Override built-in sqlite3 module
sys.modules['sqlite3'] = pysqlite3

from chromadb import Collection
from openai import OpenAI
from dotenv import load_dotenv
import os

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

def self_correct(user_query: str, model: str = "meta-llama/Llama-3.3-70B-Instruct") -> str:
    first_answer = get_response(user_query, model)
    validation_prompt = f"We asked the model the following question:\n\nQUESTION:\n{user_query}\n\nThe model answered:\n{first_answer}\n\nPlease check if the answer is correct. Respond STRICTLY with one word: 'correct' or 'incorrect'."
    validation = get_response(validation_prompt, model).strip().lower()

    if validation == "correct":
        return first_answer

    correction_prompt = f"The previous answer was marked as incorrect. Please correct it.\n\nQUESTION:\n{user_query}\n\nPrevious incorrect answer:\n{first_answer}\n\nProvide a corrected and final answer."
    corrected_answer = get_response(correction_prompt, model)

    return corrected_answer


def get_rag_response(query: str, db_collection: Collection, top_k: int = 5, distance_th: None | float = 2,  model: str= "meta-llama/Llama-3.3-70B-Instruct" ) -> tuple[str, str]:
    context_data = retirve_context_data(query, db_collection, top_k, distance_th)
    context_data = "\n\n".join(context_data)
    final_response = get_response(f"Here are example context data: {context_data}. Based on above information, answer my question: {query}. Do not output anything else.")
    return final_response, context_data


def retirve_context_data(query: str, db_collection: Collection, top_k: int = 5, distance_th: None | float = 2,) -> list[str]:
    results = db_collection.query(
    query_texts=query, # default  Chroma embedding model, TODO custom 
    n_results=top_k 
    )
    context_data = results['documents'][0]
    if distance_th is not None:
        context_data = [data   for data, distance in zip(context_data, results['distances'][0] ) if distance < distance_th  ]
    return context_data

def retirve_context_data_id(query: str, db_collection: Collection, top_k: int = 5, distance_th: None | float = 2,) -> list[str]:
    results = db_collection.query(
    query_texts=query, # default  Chroma embedding model, TODO custom 
    n_results=top_k 
    )
    context_data = results['ids'][0]
    if distance_th is not None:
        context_data = [data   for data, distance in zip(context_data, results['distances'][0] ) if distance < distance_th  ]
    return context_data
