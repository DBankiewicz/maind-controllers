from openai import OpenAI

from backend.schemas import EmailAnalysisSchema
from backend.ai_core.llm_api.api import get_response


def extract_data(model, text): 
    return get_response(text, model=model)


def process_mail(mail: str) -> EmailAnalysisSchema:
    # from 
    from_ = extract_data("meta-llama/Llama-3.3-70B-Instruct", f"Write mail addresses of sender: {mail}. This should be one email (usually after 'OD:'). Only output one mail address, no additional text") 
    # to 
    to_ = extract_data("meta-llama/Llama-3.3-70B-Instruct", f"Write mail addresses of recipents: {mail}. This should be at least one email (usually after 'DO:') at the top of the content.  Only output mail addreeses, no additional text")
    to_ = to_.split("\n")
    # topic 
    topic = extract_data("meta-llama/Llama-3.3-70B-Instruct", f"Write mail main topic: {mail}. This should be a field called 'Temat'. Only output mail title, no additional text")
    # summary 
    summary = extract_data("meta-llama/Llama-3.3-70B-Instruct", f"Summarize mail content in 3 sentences : {mail}. Only output summary, no additional text")
    # etra 
    tags = extract_data("meta-llama/Llama-3.3-70B-Instruct", f"Write potential tags, categroies: {summary}. Only output categories separated by semicolon, no additional text")

    extra = {"tags": tags}
    e = EmailAnalysisSchema(sender=from_, recepients=to_, topic=topic, summary=summary, extra=extra)
    return e