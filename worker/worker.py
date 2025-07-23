import asyncio
import concurrent.futures
import logging
import os

from dotenv import load_dotenv
from temporalio.worker import Worker

from activities.activities import AgentActivities, dynamic_tool_activity
from shared.config import TEMPORAL_TASK_QUEUE, get_temporal_client
from workflows.agent_goal_workflow import AgentGoalWorkflow


async def main():
    # Load environment variables
    load_dotenv(override=True)

    # Print LLM configuration info
    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4")
    print(f"Worker will use LLM model: {llm_model}")

    # Create the client
    client = await get_temporal_client()

    # Initialize the activities class
    activities = AgentActivities()
    print(f"AgentActivities initialized with LLM model: {llm_model}")

    print("Worker ready to process tasks!")
    logging.basicConfig(level=logging.WARN)

    # Run the worker
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue=TEMPORAL_TASK_QUEUE,
            workflows=[AgentGoalWorkflow],
            activities=[
                activities.agent_validatePrompt,
                activities.agent_toolPlanner,
                activities.get_wf_env_vars,
                dynamic_tool_activity,
            ],
            activity_executor=activity_executor,
        )

        print(f"Starting worker, connecting to task queue: {TEMPORAL_TASK_QUEUE}")
        print("Ready to begin processing...")
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
