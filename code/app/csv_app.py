import chainlit as cl
import pandas as pd
from main import crew as main_crew, rate_limit_guard  # Import the main crew object and rate limiter


@cl.on_message
async def main(message: cl.Message):
    """Handle user messages and trigger the workflows."""
    await upload_and_process_files()


@cl.step(type="run", name="File Upload Workflow")
async def upload_and_process_files():
    """Handle file uploads and trigger validation workflows based on CSV data."""
    await cl.Message(content="💬 Please upload the required CSV files: `tables.csv`, `table_schema_structure.csv`, `foreign_key_names.csv`, `primary_key_names.csv`.").send()

    # Wait for file uploads
    uploaded_files = await cl.AskFileMessage(content="Please upload the required files.", accept=["text/csv", "application/pdf"]).send()

    # Validate uploaded files
    required_files = {"tables.csv", "table_schema_structure.csv", "foreign_key_names.csv", "primary_key_names.csv"}
    uploaded_files_dict = {file.name: file for file in uploaded_files}
    missing_files = required_files - uploaded_files_dict.keys()

    if missing_files:
        await cl.Message(content=f"❌ Missing required files: {', '.join(missing_files)}").send()
        return

    try:
        # Parse uploaded files
        tables = pd.read_csv(uploaded_files_dict["tables.csv"].content)
        schema_structure = pd.read_csv(uploaded_files_dict["table_schema_structure.csv"].content)
        foreign_keys = pd.read_csv(uploaded_files_dict["foreign_key_names.csv"].content)
        primary_keys = pd.read_csv(uploaded_files_dict["primary_key_names.csv"].content)

        # Process the data and provide feedback
        await cl.Message(content=f"✅ Files successfully uploaded and processed! Starting validation workflows...").send()

        # Run the workflows with extracted metadata
        await run_workflows(tables, schema_structure, foreign_keys, primary_keys)

    except Exception as e:
        await cl.Message(content=f"❌ Error processing uploaded files: {str(e)}").send()


async def run_workflows(tables, schema_structure, foreign_keys, primary_keys):
    """Run the main validation and database workflows."""
    await run_validation_workflow(tables, schema_structure, foreign_keys, primary_keys)


@cl.step(type="run", name="Main Validation Workflow")
async def run_validation_workflow(tables, schema_structure, foreign_keys, primary_keys):
    """Run the main validation workflow using metadata from uploaded files."""
    await cl.Message(content="💬 Processing the metadata for database validation...").send()
    try:
        # Example: Passing extracted metadata as inputs
        inputs = {
            "tables": tables.to_dict(),
            "schema_structure": schema_structure.to_dict(),
            "foreign_keys": foreign_keys.to_dict(),
            "primary_keys": primary_keys.to_dict(),
        }
        result = main_crew.kickoff(inputs=inputs)
        await cl.Message(content=f"✅ Main Validation Workflow Completed Successfully!\n\n{result}").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error in Main Validation Workflow: {str(e)}").send()
        rate_limit_guard()  # Retry on failure
        try:
            result = main_crew.kickoff(inputs=inputs)
            await cl.Message(content=f"✅ Validation Workflow Completed Successfully After Retry!\n\n{result}").send()
        except Exception as retry_error:
            await cl.Message(content=f"❌ Retry Failed for Validation Workflow: {str(retry_error)}").send()
            return  # Stop further workflows if Validation fails
