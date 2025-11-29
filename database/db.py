from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from os import environ
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = environ.get("DB_USERNAME", "username")
DB_PASSWORD = environ.get("DB_PASSWORD", "password")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_PORT = environ.get("DB_PORT", 5432)
DB_NAME = environ.get("DB_NAME", "maind_controllers")

DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(DB_URL)
engine = create_engine(DB_URL)
Base = declarative_base()



