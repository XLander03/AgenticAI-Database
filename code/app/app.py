import chainlit as cl
from main import crew as main_crew, rate_limit_guard  # Import the main crew object and rate limiter
from landing_zone import landing_zone_crew  # Import the landing zone crew object
from newdb import new_db_crew  # Import the new database crew object

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages and trigger the workflows sequentially."""
    await run_workflows(message.content)

@cl.step(type="run", name="Landing Zone, Main, and New DB Workflows")
async def run_workflows(human_query: str):
    """
    Sequentially runs the Landing Zone, Main Workflow, and New Database Workflow with progress updates.
    """
    # Step 1: Run Landing Zone Workflow automatically
    await cl.Message(content="🚀 Starting Data Landing Zone Creation...").send()
    try:
        result = landing_zone_crew.kickoff()
        await cl.Message(content=f"✅ Data Landing Zone Creation Completed Successfully!\n\n{result}").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error in Data Landing Zone Creation: {str(e)}").send()
        return  # Stop the workflow if the Landing Zone step fails

    # Step 2: Prompt the user and run Main Workflow
    await cl.Message(content="💬 Provide the action to be excecuted on the database.").send()
    try:
        result = main_crew.kickoff(inputs={"query": human_query})
        await cl.Message(content=f"✅ Main Workflow Completed Successfully!\n\n{result}").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error in Main Workflow: {str(e)}").send()
        rate_limit_guard()  # Handle rate limit and retry
        try:
            result = main_crew.kickoff(inputs={"query": human_query})
            await cl.Message(content=f"✅ Database validation Completed Successfully After Retry!\n\n{result}").send()
        except Exception as retry_error:
            await cl.Message(content=f"❌ Retry Failed for Main Workflow: {str(retry_error)}").send()
            return  # Stop the workflow if retries also fail

    # Step 3: Run New Database Creation Workflow automatically
    await cl.Message(content="🚀 Starting New Database Creation...").send()
    try:
        result = new_db_crew.kickoff()
        await cl.Message(content=f"✅ New Database Creation Completed Successfully!\n\n{result}").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error in New Database Creation: {str(e)}").send()
        rate_limit_guard()
        try:
            result = new_db_crew.kickoff()
            await cl.Message(content=f"✅ New Database Creation Completed Successfully After Retry!\n\n{result}").send()
        except Exception as retry_error:
            await cl.Message(content=f"❌ Retry Failed for New Database Creation: {str(retry_error)}").send()

    await cl.Message(content="🎉 All workflows completed successfully!").send()
