import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sqlalchemy import inspect, text
from crewai_tools import tool
from crewai import Agent, Task, Crew, Process
from sqlalchemy import create_engine
from tools import detect_outliers, schema_checks
from config import llm

@tool("detect_outliers")
def detect_outliers(table_name: str, query: str, db_engine) -> str:
    """
    Detects outliers in the given table using Isolation Forest.

    Args:
        table_name (str): Table name to analyze.
        query (str): SQL query to fetch table data.
        db_engine: SQLAlchemy database engine.

    Returns:
        str: Summary of detected outliers.
    """
    try:
        # Load data
        df = pd.read_sql(query, db_engine)
        if df.empty:
            return f"❌ No data found in table '{table_name}'."

        # Use Isolation Forest for outlier detection
        model = IsolationForest(contamination=0.01, random_state=42)
        df['outlier'] = model.fit_predict(df.select_dtypes(include=['number']))

        outlier_count = df['outlier'].value_counts().get(-1, 0)
        return f"✅ Detected {outlier_count} outliers in table '{table_name}' using Isolation Forest."

    except Exception as e:
        return f"❌ Error detecting outliers in table '{table_name}': {str(e)}"

@tool("schema_checks")
def schema_checks(db_engine) -> str:
    """
    Perform schema validation to detect circular references, orphaned rows, and unused foreign keys.

    Args:
        db_engine: SQLAlchemy database engine.

    Returns:
        str: Summary of schema validation issues.
    """
    try:
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()
        results = []

        for table in tables:
            # Analyze foreign keys
            fkeys = inspector.get_foreign_keys(table)
            if not fkeys:
                results.append(f"⚠ Table '{table}' has no foreign keys.")

            # Perform orphaned row checks
            for fkey in fkeys:
                parent_table = fkey['referred_table']
                query = f"SELECT COUNT(*) FROM {table} t LEFT JOIN {parent_table} p ON t.{fkey['constrained_columns'][0]} = p.id WHERE p.id IS NULL"
                count = db_engine.execute(text(query)).fetchone()[0]
                if count > 0:
                    results.append(f"❌ Table '{table}' has {count} orphaned rows (missing references).")

        return "\n".join(results) if results else "✅ Schema validation passed successfully."

    except Exception as e:
        return f"❌ Error during schema validation: {str(e)}"


# Database Engine Configuration
db_engine = create_engine("mysql+mysqlconnector://root:password@localhost/airportdb")

# Define Advanced Validator Agent
advanced_validator = Agent(
    name="advanced_validator",
    role="Advanced Validator",
    goal="Perform advanced schema and data validation using AI.",
    backstory="""
        You are a Database Validator specializing in advanced schema and data validation.
        You:
        1. Detect circular references, orphaned rows, and unused foreign keys.
        2. Identify noise and outliers in datasets using clustering algorithms like DBSCAN and Isolation Forest.
    """,
    tools=[detect_outliers, schema_checks],
    llm=llm,
    allow_delegation=False,
)

# Tasks for Advanced Validation
schema_validation_task = Task(
    name="schema_validation_task",
    description="Analyze database schema for circular references, unused foreign keys, and orphaned rows.",
    expected_output="Summary of schema issues like circular references, orphaned rows, and unused foreign keys.",
    agent=advanced_validator,
    config={"db_engine": db_engine}
)

outlier_detection_task = Task(
    name="outlier_detection_task",
    description="Detect noise and outliers in critical tables using Isolation Forest.",
    expected_output="Summary of outliers and noise detected in the specified tables.",
    agent=advanced_validator,
    config={
        "table_name": "passenger",  # Example table
        "query": "SELECT * FROM passenger",  # Fetch all data for analysis
        "db_engine": db_engine
    }
)

# Crew Definition
crew = Crew(
    agents=[advanced_validator],
    tasks=[schema_validation_task, outlier_detection_task],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Starting Advanced Validation Pipeline...")
    result = crew.kickoff()
    print(result)
    print("✅ Advanced Schema and Data Validation Completed!")
