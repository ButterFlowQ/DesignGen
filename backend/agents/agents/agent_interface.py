from typing import List
import json

from orchestrator.models.models import ChatMessage

from ..types import AgentType, LLMResponse, LLMMessage
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

    def generate_llm_history(self, chat_history: List[ChatMessage]) -> List[LLMMessage]:
        """
        Converts the chat history into a list of messages suitable for the LLM.

        :param chat_history: The history of chat messages to transform.
        :return: A list of LLMMessage dictionaries containing 'role' and 'content'.
        """
        llm_messages: List[LLMMessage] = []

        # Add the system message as the first message
        llm_messages.append({"role": "system", "content": self.system_message})

        # Convert chat history
        for chat in chat_history:
            role = "user" if chat.is_user_message else "assistant"
            message_content = self.get_message_content(chat)
            llm_messages.append({"role": role, "content": message_content})

        return llm_messages

    def get_message_content(self, chat: ChatMessage) -> str:
        """
        Builds the appropriate message content depending on whether the sender is a user or
        an agent.

        :param chat: The ChatMessage being processed.
        :return: A string containing the relevant content for the LLM.
        """
        if chat.is_user_message:
            message = {
                "user message": chat.message,
                "document": chat.current_document.document_elements,
            }
            return json.dumps(message)

        else:
            return chat.llm_raw_response
