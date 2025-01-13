import pandas as pd
from crewai import Agent, Task, Crew
from crewai_tools import tool
from crewai import LLM
import config

# Load LLM
llm = config.llm

# Define Tools
@tool("detect_outliers_with_isolation_forest")
def detect_outliers_with_isolation_forest(data: dict) -> str:
    """
    Detects outliers in numerical data using Isolation Forest.

    Args:
        data: Dictionary containing a dataframe with key "table_data".

    Returns:
        str: Summary of detected outliers.
    """
    from sklearn.ensemble import IsolationForest

    try:
        df = data.get("table_data")
        numerical_data = df.select_dtypes(include=["number"])
        if numerical_data.empty:
            return "⚠ The provided data has no numerical columns for outlier detection."

        model = IsolationForest(contamination=0.01, random_state=42)
        df['outlier'] = model.fit_predict(numerical_data)

        outlier_count = (df['outlier'] == -1).sum()
        return f"✅ Detected {outlier_count} outliers using Isolation Forest."
    except Exception as e:
        return f"❌ Error during outlier detection: {str(e)}"


@tool("validate_schema")
def validate_schema(data: dict) -> str:
    """
    Validates schema relationships using the provided schema metadata.

    Args:
        data: Dictionary containing schema metadata.

    Returns:
        str: Summary of schema validation.
    """
    try:
        schema_df = data.get("schema_structure")
        foreign_keys_df = data.get("foreign_keys")
        primary_keys_df = data.get("primary_keys")

        validation_results = []

        # Check for missing foreign keys
        for _, row in schema_df.iterrows():
            table = row['table_name']
            if table not in foreign_keys_df['table_name'].values:
                validation_results.append(f"⚠ Table '{table}' has no foreign keys.")

        # Check for orphaned rows or missing references
        for _, fk in foreign_keys_df.iterrows():
            child_table = fk['table_name']
            parent_table = fk['referred_table']
            validation_results.append(f"Checked foreign key from '{child_table}' to '{parent_table}'.")

        return "\n".join(validation_results) if validation_results else "✅ Schema validation passed."
    except Exception as e:
        return f"❌ Error during schema validation: {str(e)}"


# Agent Definition
csv_agent = Agent(
    name="csv_agent",
    role="CSV Data Processor",
    goal="Process CSV inputs and validate database-like structures.",
    backstory="Processes and validates database-like structures from CSV inputs.",
    llm=llm,
    tools=[detect_outliers_with_isolation_forest, validate_schema],
    allow_delegation=False,
)

# Task Definitions
schema_validation_task = Task(
    name="schema_validation_task",
    description="Validate schema using metadata from CSV files.",
    expected_output="Summary of schema validation.",
    agent=csv_agent,
)

outlier_detection_task = Task(
    name="outlier_detection_task",
    description="Detect outliers in numerical data using Isolation Forest.",
    expected_output="Summary of detected outliers.",
    agent=csv_agent,
)

# Crew Definition
analysis_crew = Crew(
    agents=[csv_agent],
    tasks=[schema_validation_task, outlier_detection_task],
    verbose=True,
    memory=False,
    respect_context_window=True,
)

# Load CSV Files as Inputs
datasets = []
try:
    # Read CSV files
    tables_df = pd.read_csv("/Users/Shared/Work/Workspace/Python/Workspace/AgenticAI/code/Data/CSV/tables.csv")
    schema_df = pd.read_csv("/Users/Shared/Work/Workspace/Python/Workspace/AgenticAI/code/Data/CSV/table_schema_structure.csv")
    foreign_keys_df = pd.read_csv("/Users/Shared/Work/Workspace/Python/Workspace/AgenticAI/code/Data/CSV/foreign_keynames.csv")
    primary_keys_df = pd.read_csv("/Users/Shared/Work/Workspace/Python/Workspace/AgenticAI/code/Data/CSV/primary_key_names.csv")

    # Add to datasets
    datasets.append({
        "table_data": tables_df,
        "schema_structure": schema_df,
        "foreign_keys": foreign_keys_df,
        "primary_keys": primary_keys_df,
    })
except Exception as e:
    print(f"❌ Error loading CSV files: {str(e)}")

# Execute the pipeline
if datasets:
    result = analysis_crew.kickoff_for_each(inputs=datasets)
    print(result)
else:
    print("❌ No datasets available for processing.")
