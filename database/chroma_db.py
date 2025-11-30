

from os import environ
import chromadb
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

CHROMA_HOST = environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT = environ.get("CHROMA_PORT", 8000)

chroma = chromadb.HttpClient(host="localhost", port=8000)
collection_mails = chroma.get_or_create_collection(    name="mail",)
collection_summary_mails = chroma.get_or_create_collection(    name="summary_mails",)