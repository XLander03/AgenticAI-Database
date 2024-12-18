import pandas as pd
from sklearn.ensemble import IsolationForest
from sqlalchemy import create_engine, inspect
from crewai_tools import tool
from crewai import Agent, Task, Crew, Process
from config import llm, db

# Database Engine Configuration
db_engine = db


@tool("detect_outliers_with_isolation_forest")
def detect_outliers_with_isolation_forest(table_name: str) -> str:
    """
    Detects outliers in numerical data from the specified table using Isolation Forest.

    Args:
        table_name (str): Table name to analyze.

    Returns:
        str: Summary of detected outliers.
    """
    try:
        # Load data
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, db_engine)

        if df.empty:
            return f"❌ No data found in table '{table_name}'."

        numerical_data = df.select_dtypes(include=["number"])

        if numerical_data.empty:
            return f"⚠ Table '{table_name}' has no numerical columns for outlier detection."

        # Use Isolation Forest for outlier detection
        model = IsolationForest(contamination=0.01, random_state=42)
        df['outlier'] = model.fit_predict(numerical_data)

        outlier_count = (df['outlier'] == -1).sum()
        return f"✅ Detected {outlier_count} outliers in table '{table_name}' using Isolation Forest."
    except Exception as e:
        return f"❌ Error detecting outliers in table '{table_name}': {str(e)}"


@tool("validate_schema")
def validate_schema() -> str:
    """
    Validate the database schema and relationships.

    Returns:
        str: Summary of schema validation results.
    """
    try:
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()
        schema_summary = "Database Schema Validation Results:\n"

        for table in tables:
            fkeys = inspector.get_foreign_keys(table)
            schema_summary += f"Table '{table}':\n"
            if fkeys:
                schema_summary += f"  Foreign Keys: {fkeys}\n"
            else:
                schema_summary += "  ⚠ No foreign keys found.\n"

        return schema_summary
    except Exception as e:
        return f"❌ Error during schema validation: {str(e)}"


# Define Simplified Validator Agent
advanced_validator = Agent(
    name="advanced_validator",
    role="Advanced Schema and Data Validator",
    goal="Perform schema validation and detect outliers in numerical data.",
    backstory="""
        You are an advanced database validator with expertise in:
        1. Schema validation for missing foreign keys and relationships.
        2. Data analysis using Isolation Forest for outlier detection in numerical columns.
    """,
    tools=[detect_outliers_with_isolation_forest, validate_schema],
    llm=llm,
    allow_delegation=False,
)

# Define Tasks
schema_validation_task = Task(
    name="schema_validation_task",
    description="Validate the database schema for missing keys and relationships.",
    expected_output="Summary of schema validation, including missing relationships and foreign keys.",
    agent=advanced_validator
)

outlier_detection_task = Task(
    name="outlier_detection_task",
    description="Detect outliers in numerical data from a specific table using Isolation Forest.",
    expected_output="Summary of detected outliers using Isolation Forest.",
    agent=advanced_validator,
    config={"table_name": "passenger"}  # Example table for analysis
)

# Crew Definition
crew = Crew(
    agents=[advanced_validator],
    tasks=[schema_validation_task, outlier_detection_task],
    process=Process.sequential,
    verbose=True
)

# Main Execution
if __name__ == "__main__":
    print("🚀 Starting Schema and Data Validation Workflow...")
    result = crew.kickoff()
    print(result)
    print("✅ Workflow Completed Successfully!")
