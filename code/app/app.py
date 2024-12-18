import chainlit as cl
from main import crew, rate_limit_guard  # Import the reusable crew object

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages and trigger the crew workflow."""
    await chainlit_run(message.content)

@cl.step(type="run", name="Data Validation Workflow")
async def chainlit_run(human_query: str):
    """
    Runs the crew.kickoff() process dynamically and handles rate limit retries.
    """
    try:
        # Run the crew workflow
        result = crew.kickoff(inputs={"query": human_query})
    except Exception as e:
        print(f"Rate limit error or exception: {e}")
        rate_limit_guard()
        result = crew.kickoff(inputs={"query": human_query})
    
    # Send the results as a markdown message
    await cl.Message(content=result.to_markdown(), author="Data Analyst").send()
