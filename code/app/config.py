import os
from sqlalchemy import create_engine, inspect
from langchain_community.utilities.sql_database import SQLDatabase
from pydantic_settings import BaseSettings, SettingsConfigDict
from crewai import LLM

class Settings(BaseSettings):
    groq_api_key: str
    db_uri: str
    azure_api_key: str
    azure_api_base: str
    azure_api_version: str

    class Config:
        env_file = f'.env.{os.getenv("ENVIRONMENT", "development")}'
        extra = "ignore"

settings = Settings()

os.environ["GROQ_API_KEY"] = settings.groq_api_key
DB_URI = settings.db_uri

db = SQLDatabase.from_uri(DB_URI)

os.environ['AZURE_API_KEY'] = settings.azure_api_key
os.environ["AZURE_API_BASE"] = settings.azure_api_base
os.environ["AZURE_API_VERSION"] = settings.azure_api_version

llm = LLM(model="azure/gpt4O", api_version=settings.azure_api_version, base_url=settings.azure_api_base)