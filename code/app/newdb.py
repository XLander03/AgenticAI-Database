from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from config import llm 
from sqlalchemy import create_engine, text, inspect
from crewai_tools import tool
import config

db_engine = create_engine(config.DB_URI)
# ---------------------- TOOLS ----------------------
@tool("copy_database")
def copy_database(new_db_name: str) -> str:
    """
    Creates a new database, copies all tables and their data from the existing database,
    and applies corrections.

    Args:
        new_db_name (str): The name for the new database.

    Returns:
        str: Success message or an error message if the operation fails.
    """
    try:
        current_engine = db_engine
        with current_engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {new_db_name}"))
            print(f"✅ Database '{new_db_name}' created successfully!")

        new_db_url = current_engine.url.set(database=new_db_name)
        new_engine = create_engine(new_db_url)

        inspector = inspect(current_engine)
        tables = inspector.get_table_names()

        for table in tables:
            with current_engine.connect() as conn:
                copy_query = f"CREATE TABLE {new_db_name}.{table} AS SELECT * FROM {table}"
                conn.execute(text(copy_query))
                print(f"✅ Table '{table}' copied successfully to '{new_db_name}'.")

        current_engine.dispose()
        new_engine.dispose()

        return f"✅ The database has been successfully copied to '{new_db_name}'."
    except Exception as e:
        return f"❌ Error saving the database: {str(e)}"


database_expert = Agent(
    name="database_expert",
    role="Database Expert",
    goal="Create a new database and copy all data from the source database.",
    backstory="""
        You are a database expert tasked with copying an entire database into a new one.
        Use the `copy_database` tool to create a full backup and save the fixed version.
    """,
    tools=[copy_database],
    llm=llm,
    allow_delegation=False,
)

save_corrected_db = Task(
    name="save_corrected_db",
    description="Create a new database named 'fixed_<source_db>' and copy all tables into it.",
    expected_output="The corrected database has been saved successfully.",
    agent=database_expert,
    config={"new_db_name": "fixed_airportdb"},
)

new_db_crew = Crew(
    agents=[database_expert],
    tasks=[save_corrected_db],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Starting New Database Creation Pipeline...")
    result = new_db_crew.kickoff()
    print(result)
    print("✅ New database creation pipeline completed successfully!")
