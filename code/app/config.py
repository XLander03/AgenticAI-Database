import os
from sqlalchemy import create_engine, inspect
from langchain_community.utilities.sql_database import SQLDatabase
# Required
os.environ["GROQ_API_KEY"] = "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"
DB_URI = "mysql+mysqlconnector://root:9009@localhost:3306/airportdb"

db = SQLDatabase.from_uri(DB_URI)
llm = "groq/llama-3.3-70b-versatile"



