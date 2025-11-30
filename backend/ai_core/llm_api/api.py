import pysqlite3
import sys

from backend.ai_core.graphs.build_dag import async_build_dag
from backend.ai_core.graphs.extras import assign_topic_tags, calculate_rolling_states
from backend.schemas.mail import EmailWithAnalysis
from backend.ai_core.llm_api.helper import get_response
# Override built-in sqlite3 module
sys.modules['sqlite3'] = pysqlite3

from chromadb import Collection
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

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


async def get_timeline_changes(emails_full: list[EmailWithAnalysis]) -> str:
    emails = [e.analysis for  e in emails_full if e.analysis is not None]
    dag_connections = await async_build_dag(emails)
    rolling_states = calculate_rolling_states(emails, dag_connections)
    topic_tags = assign_topic_tags(emails, dag_connections)

    response = ""
    
    response += "DAG Connections:\n"
    for c in dag_connections:
        response += f"Email: {c.older_email.id} --> Email: {c.newer_email.id}\n"
        response += f"decisions: {c.decisions}\n"
        response += f"risks: {c.risks}\n"
        response += f"inquiries: {c.inquiries}\n"
        response += "-----\n"


    response += "\nRolling States:\n"
    for e in emails:
        response += f"Email: {e.id} --> Rolling State: {rolling_states.get(e, 'No State')}\n"

    response += "\nTopic Tags:\n"
    for email, topics in topic_tags.items():
        response += f"Email: {email.id}\n"
        response += f"Topics: {';; '.join(topics)}\n"
        response += "-----\n"
    
    return response