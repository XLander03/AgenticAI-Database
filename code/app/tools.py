from crewai_tools import tool
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from crewai_tools import tool
from config import  db, llm
import pandas as pd
import subprocess

@tool("list_tables")
def list_tables() -> str:
    """List the available tables in the database."""
    return ListSQLDatabaseTool(db=db).invoke("")

@tool("tables_schema")
def tables_schema(tables: str) -> str:
    """
    Input is a comma-separated list of tables; output is the schema and sample rows.
    """
    tool = InfoSQLDatabaseTool(db=db)
    return tool.invoke(tables)

@tool("execute_sql")
def execute_sql(sql_query: str) -> str:
    """Execute a SQL query against the database."""
    return QuerySQLDataBaseTool(db=db).invoke(sql_query)

@tool("check_sql")
def check_sql(sql_query: str) -> str:
    """Check if the SQL query is correct."""
    return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})

@tool("read_schema_csv")
def read_schema_csv(file_path: str) -> dict:
    """
    Reads a CSV file containing modified schema definitions and returns it as a dictionary.
    Args:
        file_path (str): The path to the CSV file containing the schema.
    Returns:
        dict: A dictionary containing table names and their corresponding schema definitions.
    """
    try:
        df = pd.read_csv(file_path)
        schema = df.to_dict(orient="records")
        return {"status": "success", "schema": schema}
    except Exception as e:
        return {"status": "error", "message": str(e)}


