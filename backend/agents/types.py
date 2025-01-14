from enum import Enum, auto
from typing import Any, TypedDict


class AgentType(Enum):
    """
    An enumeration representing various agent types in the system.
    """

    USER = auto()
    REQUIREMENT = auto()
    ARCHITECTURE = auto()
    DATABASE = auto()


class LLMMessage(TypedDict):
    """
    A message passed to or from an LLM, consisting of a role and its content.

    Attributes:
        role: Indicates the message role ("system", "user", or "assistant").
        content: The text content of the message.
    """

    role: str
    content: str


class LLMResponse(TypedDict):
    """
    A structured response from the LLM, containing:
      1) The updated workflow document state.
      2) A response message (often returned to the user).
      3) A flag indicating whether to proceed to the next workflow step.

    Attributes:
        updated_workflow_doc: The updated document or workflow state.
            Use Any if the structure can vary, or a more specific type if known.
        response_message: The LLM's response message or summary.
        move_to_next_workflow: Whether the workflow should advance to the next step.
    """

    updated_workflow_doc: Any
    response_message: str
    move_to_next_workflow: bool
    agent_id: str
