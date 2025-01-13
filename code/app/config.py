import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_community.utilities.sql_database import SQLDatabase
from pydantic_settings import BaseSettings, SettingsConfigDict
from crewai import LLM

# Explicitly load .env for debugging
load_dotenv(".env")

class Settings(BaseSettings):
    groq_api_key: str
    db_uri: str
    azure_api_key: str
    azure_api_base: str
    azure_api_version: str
    openai_api_key: str

    model_config = SettingsConfigDict(env_file="/Users/Shared/Work/Workspace/Python/Workspace/AgenticAI/code/app/.env", extra="ignore", )


settings = Settings()



# Configure LLM
llm = LLM(
    model="openai/gpt-4o",  # or "gpt4O" depending on usage
    temperature=0.7,
    api_key=settings.openai_api_key,
)
