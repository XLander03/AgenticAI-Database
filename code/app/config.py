import os
from sqlalchemy import create_engine, inspect
from langchain_community.utilities.sql_database import SQLDatabase
# Required
os.environ["GROQ_API_KEY"] = "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"
DB_URI = "mysql+mysqlconnector://root:9009@localhost:3306/new_airportdb"

db = SQLDatabase.from_uri(DB_URI)
#llm = "groq/llama-3.3-70b-versatile"
from crewai import LLM

AZURE_API_KEY="e4ea23b7b3ba480bba8737c165d172b2"
AZURE_API_BASE="https://cmhq-openai.openai.azure.com/"
AZURE_API_VERSION="2024-08-01-preview"
os.environ['AZURE_API_KEY'] = AZURE_API_KEY
os.environ["AZURE_API_BASE"] = AZURE_API_BASE
os.environ["AZURE_API_VERSION"] = AZURE_API_VERSION

llm = LLM(model="azure/gpt4O", api_version=AZURE_API_VERSION, base_url=AZURE_API_BASE)
