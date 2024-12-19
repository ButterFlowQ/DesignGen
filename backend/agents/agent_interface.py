from typing import List
from .types import ChatMessage, AgentType, LLMResponse


class AgentInterface:
    def __init__(
        self,
        system_message: str,
        agent_type: AgentType,
    ) -> None:
        self.system_message = {
            "role": "system",
            "content": system_message,
        }
        self.agent_type = agent_type

    def process(
        self,
        chat_history: List[ChatMessage],
    ) -> LLMResponse:
        pass
