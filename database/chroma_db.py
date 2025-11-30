

from os import environ
import pysqlite3
import sys

# Override built-in sqlite3 module
sys.modules['sqlite3'] = pysqlite3

import chromadb
from dotenv import load_dotenv
import time
import logging
from pydantic import BaseModel

load_dotenv()

CHROMA_HOST = environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT = int(environ.get("CHROMA_PORT", 8000))

# Try connecting to Chroma with a few retries in case the server isn't ready yet.
logger = logging.getLogger("chroma_db")
chroma = None
for attempt in range(10):
	try:
		chroma = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
		break
	except Exception as e:
		logger.warning("Chroma not available yet (attempt %d): %s", attempt + 1, e)
		time.sleep(1)
if chroma is None:
	# If we couldn't connect, raise a runtime error so the app startup explicitly fails.
	raise RuntimeError(f"Could not connect to a Chroma server at {CHROMA_HOST}:{CHROMA_PORT}")
collection_mails = chroma.get_or_create_collection(name="mail",)
collection_summary_mails = chroma.get_or_create_collection(name="summary_mails",)