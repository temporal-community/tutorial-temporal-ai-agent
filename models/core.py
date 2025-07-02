from dataclasses import dataclass
from typing import List


@dataclass
class ToolArgument:
    name: str
    type: str
    description: str


@dataclass
class ToolDefinition:
    name: str
    description: str
    arguments: List[ToolArgument]


@dataclass
class AgentGoal:
    id: str
    agent_name: str
    tools: List[ToolDefinition]
    description: str
    starter_prompt: str
    example_conversation_history: str
