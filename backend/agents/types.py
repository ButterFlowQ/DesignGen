from enum import Enum, auto
from typing import Any, TypedDict


class AgentType(str, Enum):
    """
    An enumeration representing various agent types in the system.
    """

    USER = "user"
    FUNCTIONAL_REQUIREMENT = auto()
    NON_FUNCTIONAL_REQUIREMENT = auto()
    ARCHITECTURE = auto()
    API_CONTRACT = auto()
    DATABASE_SCHEMA = auto()
    HTML_GENERATOR = auto()


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
      1) The updated document element state.
      2) A response message (often returned to the user).
      3) The raw response from the LLM.

    Attributes:
        updated_doc_element: The updated document element state.
            Use Any if the structure can vary, or a more specific type if known.
        response_message: The LLM's response message or summary.
        raw_response: The raw response from the LLM.
    """

    updated_doc_element: Any
    response_message: str
    raw_response: str
