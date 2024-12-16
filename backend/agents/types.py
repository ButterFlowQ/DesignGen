from typing import TypedDict
from enum import Enum

class AgentType(Enum):
    User = 1
    Requirement = 2
    Database = 3
    
class ChatMessage(TypedDict):
    agent_id: AgentType
    message: str
    document: any # complete current state of document
    response: str # response from the LLM

class LLMMessage(TypedDict):
    role: str  # can be "system", "user", or "assistant"
    content: str

class LLMResponse(TypedDict):
    move_to_next_workflow: bool  # indicates whether to proceed to next workflow step
    response_message: str        # the response message from the LLM
    updated_workflow_doc: any    # the updated workflow document state
