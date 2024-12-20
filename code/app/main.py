import yaml
from crewai import Agent, Crew, Task, Process
from tools import list_tables, tables_schema, execute_sql, check_sql
import config
import time

llm = config.llm

def rate_limit_guard():
    print("Rate limit hit. Retrying in 60 seconds...")
    time.sleep(60)

with open("config.yaml", "r") as file:
    yaml_config = yaml.safe_load(file)

tools = {
    "list_tables": list_tables,
    "tables_schema": tables_schema,
    "execute_sql": execute_sql,
    "check_sql": check_sql
}

# Define Agents
sql_dev = Agent(
    name="sql_dev",
    role="Senior Database Developer",
    goal="Construct and execute SQL queries to analyze and validate the database schema and data.",
    backstory=yaml_config["agents"]["sql_dev"]["backstory"],
    llm=llm,
    tools=[tools["list_tables"], tools["tables_schema"], tools["execute_sql"], tools["check_sql"]],
    allow_delegation=False,
)

data_validator = Agent(
    name="data_validator",
    role="Data Quality Specialist",
    goal="Detect and validate data issues and provide detailed quality statistics.",
    backstory=yaml_config["agents"]["data_validator"]["backstory"],
    llm=llm,
    tools=[],  
    allow_delegation=False,
)

schema_validator = Agent(
    name="schema_validator",
    role="Schema Validator",
    goal="Ensure schema relationships are logically consistent and aligned with real-world business rules.",
    backstory=yaml_config["agents"]["schema_validator"]["backstory"],
    llm=llm,
    tools=[tools["list_tables"], tools["tables_schema"]],  
    allow_delegation=False,
)

database_expert = Agent(
    name="database_expert",
    role="Database Expert",
    goal="Fix database issues and save the corrected database into a new one.",
    backstory=yaml_config["agents"]["database_expert"]["backstory"],
    llm=llm,
    tools=[tools["execute_sql"], tools["check_sql"]],
    allow_delegation=False,
)
    
prompt_modifier = Agent(
    name="prompt_modifier",
    role="Agent Prompt Modifier",
    goal="Incorporate user modifications (ground truth relationships) into validation prompts and regenerate SQL queries.",
    backstory=yaml_config["agents"]["prompt_modifier"]["backstory"],
    llm=llm,
    tools=[tools["tables_schema"]],  
    allow_delegation=False,
)

report_writer = Agent(
    name="report_writer",
    role="Report Writer",
    goal="Summarize the results of schema and data validation and the database fixes into actionable insights.",
    backstory=yaml_config["agents"]["report_writer"]["backstory"],
    llm=llm,
    tools=[],  
    allow_delegation=False,
)

# Define Tasks
generate_sql = Task(
    name="generate_sql",
    description=yaml_config["tasks"]["generate_sql"]["description"],
    expected_output=yaml_config["tasks"]["generate_sql"]["expected_output"],
    agent=sql_dev,
)

validate_data = Task(
    name="validate_data",
    description=yaml_config["tasks"]["validate_data"]["description"],
    expected_output=yaml_config["tasks"]["validate_data"]["expected_output"],
    agent=data_validator,
    context=[generate_sql],
)

validate_schema = Task(
    name="validate_schema",
    description=yaml_config["tasks"]["validate_schema"]["description"],
    expected_output=yaml_config["tasks"]["validate_schema"]["expected_output"],
    agent=schema_validator,
    context=[generate_sql],
)

generate_fix_sql = Task(
    name="generate_fix_sql",
    description=yaml_config["tasks"]["generate_fix_sql"]["description"],
    expected_output=yaml_config["tasks"]["generate_fix_sql"]["expected_output"],
    agent=prompt_modifier,
    context=[validate_schema],
)

apply_ground_truth = Task(
    name="apply_ground_truth",
    description=yaml_config["tasks"]["apply_ground_truth"]["description"],
    expected_output=yaml_config["tasks"]["apply_ground_truth"]["expected_output"],
    agent=database_expert,
    context=[generate_fix_sql],
)

summarize_results = Task(
    name="summarize_results",
    description=yaml_config["tasks"]["summarize_results"]["description"],
    expected_output=yaml_config["tasks"]["summarize_results"]["expected_output"],
    agent=report_writer,
    context=[validate_data, validate_schema, generate_fix_sql, apply_ground_truth],
)

crew = Crew(
    agents=[sql_dev, data_validator, schema_validator, database_expert, prompt_modifier, report_writer],
    tasks=[generate_sql, validate_data, validate_schema, generate_fix_sql, apply_ground_truth, summarize_results],
    process=Process.sequential,
    verbose=True,
    output_log_file="crew.log",
)

"""
if __name__ == "__main__":
    inputs = {"query": "Validate the airportdb database"}
    try:
        result = crew.kickoff(inputs=inputs)
    except Exception as e:
        print(f"Error: {e}")
        rate_limit_guard()
        result = crew.kickoff(inputs=inputs)
    print("Workflow completed successfully!")
"""


