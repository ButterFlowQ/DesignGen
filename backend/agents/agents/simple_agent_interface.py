from typing import List

from ..types import AgentType, LLMResponse, LLMMessage
from ..llm_wrapper import LLMWrapper


class SimpleAgentInterface:
    def __init__(
        self,
        agent_type: AgentType,
        system_message: str,
        response_format: list[str],
        model: str = None,
    ) -> None:
        self.system_message = system_message
        self.agent_type = agent_type
        self.response_format = response_format
        if model:
            self.llm = LLMWrapper(model)
        else:
            self.llm = LLMWrapper()

    def process(
        self,
        message: str,
    ) -> LLMResponse:
        pass

    def generate_llm_history(self, message: str) -> List[LLMMessage]:
        """
        Converts the message into a list of messages suitable for the LLM.

        :param message: The message to transform.
        :return: A list of LLMMessage dictionaries containing 'role' and 'content'.
        """
        llm_messages: List[LLMMessage] = []

        # Add the system message as the first message
        llm_messages.append({"role": "user", "content": self.system_message})
        llm_messages.append(LLMMessage(role="user", content=message))

        return llm_messages
