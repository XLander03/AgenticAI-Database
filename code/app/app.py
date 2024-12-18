import chainlit as cl
from main import crew as main_crew, rate_limit_guard  # Import the main crew object and rate limiter
from landing_zone import landing_zone_crew  # Import the landing zone crew object
from newdb import new_db_crew  # Import the new database crew object

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages and trigger the workflows sequentially."""
    await run_workflows(message.content)

@cl.step(type="run", name="Data Validation and Database Workflow")
async def run_workflows(human_query: str):
    """
    Sequentially runs the Landing Zone, Main Workflow, and New Database Workflow with progress updates.
    """
    workflows = [
        ("Data Landing Zone Creation", landing_zone_crew),
        ("Data Validation Workflow", main_crew),
        ("New Database Creation", new_db_crew),
    ]

    for workflow_name, workflow_crew in workflows:
        await cl.Message(content=f"🚀 Starting {workflow_name}...").send()
        try:
            result = workflow_crew.kickoff(inputs={"query": human_query})
            await cl.Message(content=f"✅ {workflow_name} Completed Successfully!\n\n{result.to_markdown()}").send()
        except Exception as e:
            await cl.Message(content=f"❌ Error in {workflow_name}: {str(e)}").send()
            rate_limit_guard()  # Handle rate limit and retry
            try:
                result = workflow_crew.kickoff(inputs={"query": human_query})
                await cl.Message(content=f"✅ {workflow_name} Completed Successfully After Retry!\n\n{result.to_markdown()}").send()
            except Exception as retry_error:
                await cl.Message(content=f"❌ Retry Failed for {workflow_name}: {str(retry_error)}").send()
                return  # Stop the workflow if retries also fail

    await cl.Message(content="🎉 All workflows completed successfully!").send()
