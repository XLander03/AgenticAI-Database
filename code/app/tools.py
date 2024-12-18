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


@tool("copy_database")
def copy_database(new_db_name: str, source_db_name: str, user: str, password: str, host: str = "localhost") -> str:
    """
    Creates a full copy of the source database into a new database using mysqldump.

    Args:
        new_db_name (str): The name of the new database.
        source_db_name (str): The name of the source database.
        user (str): Database username.
        password (str): Database password.
        host (str): Database host.

    Returns:
        str: Success or error message.
    """
    try:
        # Step 1: Create the new database
        create_db_command = f"mysql -u{user} -p{password} -h {host} -e 'CREATE DATABASE {new_db_name};'"
        subprocess.run(create_db_command, shell=True, check=True)
        print(f"✅ Database '{new_db_name}' created successfully!")

        # Step 2: Use mysqldump to copy the data
        dump_command = (
            f"mysqldump -u{user} -p{password} -h {host} {source_db_name} "
            f"| mysql -u{user} -p{password} -h {host} {new_db_name}"
        )
        subprocess.run(dump_command, shell=True, check=True)
        print(f"✅ Database '{source_db_name}' copied successfully to '{new_db_name}'!")

        return f"✅ The database has been successfully copied to '{new_db_name}'."
    except subprocess.CalledProcessError as e:
        return f"❌ Error copying the database: {str(e)}"

