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
