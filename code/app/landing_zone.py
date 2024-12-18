import os
import pandas as pd
from crewai import Agent, Crew, Task, Process
from crewai_tools import tool
from textwrap import dedent
from sqlalchemy import create_engine, inspect
import time
import config


db_engine = create_engine(config.DB_URI)
os.environ["GROQ_API_KEY"] = "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"

@tool("export_tables_to_landing_zone")
def export_tables_to_landing_zone(folder_path: str) -> str:
    """
    Exports all tables from the database into the specified folder as CSV files.
    Ensures data completeness by saving a copy of raw data.
    """
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Use the SQLAlchemy inspector to fetch table names
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()

        # Export each table to CSV
        for table in tables:
            print(table)
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, db_engine)
            file_path = os.path.join(folder_path, f"{table}.csv")
            df.to_csv(file_path, index=False)
            print(f"✅ Exported table '{table}' to {file_path}")

        return f"Successfully exported {len(tables)} tables to the Landing Zone: {folder_path}"
    except Exception as e:
        return f"❌ Error exporting tables: {str(e)}"

# Agent: Data Extraction Specialist
data_extraction_agent = Agent(
    role="Data Extraction Specialist",
    goal="Create a Landing Zone and transfer raw data tables from the database.",
    backstory=dedent("""
        You are responsible for ensuring raw data integrity by exporting all tables from the database into a secure 
        Landing Zone folder. You identify all tables, extract data, and store them as CSV files while maintaining completeness.
    """),
    llm="groq/llama-3.3-70b-versatile",
    tools=[export_tables_to_landing_zone],
    allow_delegation=False,
)

# Task: Export Data to Landing Zone
data_landing_zone_task = Task(
    description="Export all database tables into a Landing Zone folder as CSV files.",
    expected_output=dedent("""
        All database tables have been exported to the Landing Zone folder.
        The output includes:
        - Table names
        - Path to each exported CSV file
        """),
    agent=data_extraction_agent,
    config={"folder_path": "./Landing_zone"}  # Default folder path for Landing Zone
)

# Crew Definition
landing_zone_crew = Crew(
    agents=[data_extraction_agent],
    tasks=[data_landing_zone_task],
    process=Process.sequential,
    verbose=True
)

# Rate Limiting Guard
def rate_limit_guard():
    """Waits for the rate limit window to reset."""
    print("⏳ Rate limit reached. Waiting for 60 seconds...")
    time.sleep(60)

# Main Execution
if __name__ == "__main__":
    print("🚀 Starting Data Landing Zone Creation...")
    try:
        result = landing_zone_crew.kickoff()
        print("✅ Landing Zone Creation Completed!")
        print(result)
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        rate_limit_guard()
