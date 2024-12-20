import chainlit as cl
from main import crew as main_crew, rate_limit_guard  # Import the main crew object and rate limiter
from landing_zone import landing_zone_crew  # Import the landing zone crew object
from newdb import new_db_crew  # Import the new database crew object
from ml_checks import ml_crew  # Import the ML checks crew object

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages and trigger the workflows sequentially."""
    await start_landing_zone_workflow()
    await run_validation_workflow(message.content)
    await run_ml_checks_workflow()
    await start_new_db_workflow()

@cl.step(type="run", name="Data Landing Zone Workflow")
async def start_landing_zone_workflow():
    """Run the Data Landing Zone Workflow."""
    await cl.Message(content="🚀 Starting Data Landing Zone Creation...").send()
    try:
        result = landing_zone_crew.kickoff()
        await cl.Message(content=f"✅ Data Landing Zone Creation Completed Successfully!\n\n{result}").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error in Data Landing Zone Creation: {str(e)}").send()
        return  

@cl.step(type="run", name="Main Validation Workflow")
async def run_validation_workflow(human_query: str):
    """Run the main validation workflow after receiving user input."""

    try:
        async_function = cl.make_async(main_crew.kickoff)
        result = await async_function({"query": human_query})
        await cl.Message(content=f"✅ Database Validation Completed Successfully!\n\n{result}").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error in Main Workflow: {str(e)}").send()
        rate_limit_guard()  # Retry on failure
        try:
            result = main_crew.kickoff(inputs={"query": human_query})
            await cl.Message(content=f"✅ Database Validation Completed Successfully After Retry!\n\n{result}").send()
        except Exception as retry_error:
            await cl.Message(content=f"❌ Retry Failed for Main Workflow: {str(retry_error)}").send()
            return 


@cl.step(type="run", name="ML Checks Workflow")
async def run_ml_checks_workflow():
    """Run the Machine Learning Checks Workflow."""
    await cl.Message(content="🚀 Starting Machine Learning Checks...").send()
    try:
        result = ml_crew.kickoff()
        await cl.Message(content=f"✅ Machine Learning Checks Completed Successfully!\n\n{result}").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error in Machine Learning Checks: {str(e)}").send()
        rate_limit_guard()  # Retry on failure
        try:
            result = ml_crew.kickoff()
            await cl.Message(content=f"✅ Machine Learning Checks Completed Successfully After Retry!\n\n{result}").send()
        except Exception as retry_error:
            await cl.Message(content=f"❌ Retry Failed for Machine Learning Checks: {str(retry_error)}").send()
            return  


@cl.step(type="run", name="New Database Workflow")
async def start_new_db_workflow():
    """Run the New Database Creation Workflow."""
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

if __name__ == '__main__':
    while True:
        pass