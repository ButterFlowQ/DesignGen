from typing import TypedDict
from enum import Enum


class AgentType(Enum):
    USER = 1
    REQUIREMENT = 2
    DATABASE = 3

class LLMMessage(TypedDict):
    role: str  # can be "system", "user", or "assistant"
    content: str


class LLMResponse(TypedDict):
    updated_workflow_doc: any  # the updated workflow document state
    response_message: str  # the response message from the LLM
    move_to_next_workflow: bool  # indicates whether to proceed to next workflow step
