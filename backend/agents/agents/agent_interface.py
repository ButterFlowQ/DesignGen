from typing import List

from workflowManager.models.models import ChatMessage

from ..types import AgentType, LLMResponse
from ..llm_wrapper import LLMWrapper


class AgentInterface:
    def __init__(
        self,
        agent_type: AgentType,
        system_message: str,
        response_format: list[str],
    ) -> None:
        self.system_message = system_message
        self.agent_type = agent_type
        self.response_format = response_format
        self.llm = LLMWrapper()

    def process(
        self,
        chat_history: List[ChatMessage],
    ) -> LLMResponse:
        pass
