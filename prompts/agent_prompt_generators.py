import json
from typing import Optional

from models.core import AgentGoal
from models.requests import ConversationHistory, ToolData
from prompts.prompts import GENAI_PROMPT, MISSING_ARGS_PROMPT, TOOL_COMPLETION_PROMPT


def generate_genai_prompt(
    agent_goal: AgentGoal,
    conversation_history: ConversationHistory,
    raw_json: Optional[ToolData] = None,
) -> str:
    """
    Generates a concise prompt for producing or validating JSON instructions
    with the provided tools and conversation history.
    """

    # Prepare template variables
    template_vars = {
        "agent_goal": agent_goal,
        "conversation_history_json": json.dumps(conversation_history, indent=2),
        "toolchain_complete_guidance": generate_toolchain_complete_guidance(),
        "raw_json": raw_json,
        "raw_json_str": (
            json.dumps(raw_json, indent=2) if raw_json is not None else None
        ),
    }

    return GENAI_PROMPT.render(**template_vars)


def generate_tool_completion_prompt(current_tool: str, dynamic_result: dict) -> str:
    """
    Generates a prompt for handling tool completion and determining next steps.

    Args:
        current_tool: The name of the tool that just completed
        dynamic_result: The result data from the tool execution

    Returns:
        str: A formatted prompt string for the agent to process the tool completion
    """
    return TOOL_COMPLETION_PROMPT.format(
        current_tool=current_tool, dynamic_result=dynamic_result
    )


def generate_missing_args_prompt(
    current_tool: str, tool_data: dict, missing_args: list[str]
) -> str:
    """
    Generates a prompt for handling missing arguments for a tool.

    Args:
        current_tool: The name of the tool that needs arguments
        tool_data: The current tool data containing the response
        missing_args: List of argument names that are missing

    Returns:
        str: A formatted prompt string for requesting missing arguments
    """
    return MISSING_ARGS_PROMPT.format(
        response=tool_data.get("response"),
        current_tool=current_tool,
        missing_args=missing_args,
    )


def generate_toolchain_complete_guidance() -> str:
    """
    Generates a prompt for guiding the LLM to handle the end of the toolchain.

    Args:
        None

    Returns:
        str: A prompt string prompting the LLM to prompt for a new goal, or be done
    """
    return "If no more tools are needed (user_confirmed_tool_run has been run for all), set next='done' and tool=''."
