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
    config = yaml.safe_load(file)

tools = {
    "list_tables": list_tables,
    "tables_schema": tables_schema,
    "execute_sql": execute_sql,
    "check_sql": check_sql
}

agents = {}
for agent_config in config["agents"]:
    agents[agent_config["name"]] = Agent(
        role=agent_config["role"],
        goal=agent_config["goal"],
        backstory=agent_config["backstory"],
        llm=llm,
        tools=[tools[tool_name] for tool_name in tools.keys() if tool_name in agent_config.get("backstory", "")],
        allow_delegation=False,
    )

tasks = []
for task_config in config["tasks"]:
    agent_name = task_config["agent"]
    tasks.append(Task(
        description=task_config["description"],
        expected_output=task_config["expected_output"],
        agent=agents[agent_name],
        config=task_config.get("config", {}),
        #context=task_config.get("context", []),
    ))

crew = Crew(
    agents=list(agents.values()),
    tasks=tasks,
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


