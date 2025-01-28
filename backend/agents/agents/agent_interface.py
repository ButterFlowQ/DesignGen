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
        chat_history: List[ChatMessage],
    ) -> LLMResponse:
        pass

    def generate_llm_history(self, chat_history: List[ChatMessage], agent_type: AgentType = None) -> List[LLMMessage]:
        """
        Converts the chat history into a list of messages suitable for the LLM.

        :param chat_history: The history of chat messages to transform.
        :return: A list of LLMMessage dictionaries containing 'role' and 'content'.
        """
        llm_messages: List[LLMMessage] = []

        # Add the system message as the first message
        llm_messages.append({"role": "user", "content": self.system_message})

        # Convert chat history
        for chat in chat_history:
            role = "user" if chat.is_user_message else "assistant"
            message_content = self.get_message_content(chat, agent_type)
            llm_messages.append({"role": role, "content": message_content})

        return llm_messages

    def get_message_content(self, chat: ChatMessage, agent_type: AgentType) -> str:
        """
        Builds the appropriate message content depending on whether the sender is a user or
        an agent.

        :param chat: The ChatMessage being processed.
        :param agent_type: The type of agent processing the message.
        :return: A string containing the relevant content for the LLM.
        """
        document_elements = {}
        match agent_type:
            # Requirements specific
            case AgentType.FUNCTIONAL_REQUIREMENT:
                keys = ["functional requirements", "non functional requirements", "architecture", "api contracts", "database schema"]
            case AgentType.NON_FUNCTIONAL_REQUIREMENT:
                keys = ["functional requirements", "non functional requirements", "architecture", "api contracts", "database schema"]
            # Architecture and Schema
            case AgentType.ARCHITECTURE:
                keys = ["functional requirements", "non functional requirements", "architecture", "api contracts", "database schema"]
            case AgentType.API_CONTRACT:
                keys = ["functional requirements", "non functional requirements", "architecture", "api contracts", "database schema"]
            case AgentType.DATABASE_SCHEMA:
                keys = ["functional requirements", "non functional requirements", "architecture", "api contracts", "database schema"]
            # LLD specific
            case AgentType.JAVA_LLD:
                keys = ["functional requirements", "non functional requirements", "architecture", "api contracts", "database schema", "java LLD"]
            case AgentType.REACT_LLD:
                keys = ["functional requirements", "architecture", "api contracts", "react LLD"]
            # Code generators
            case AgentType.JAVA_CODE_GENERATOR:
                keys = ["functional requirements", "non functional requirements", "architecture", "api contracts", "database schema", "java code", "java LLD"]
            case AgentType.REACT_CODE_GENERATOR:
                keys = ["functional requirements", "architecture", "api contracts", "react code", "react LLD"]
            # User or default case
            case _:
                raise NotImplementedError(f"Agent type '{agent_type}' is not supported for message content generation")
        
        document_elements = {k: v for k, v in chat.current_document.document_elements.items() if k in keys}

        if chat.is_user_message:
            message = {
                "user message": chat.message,
                "document": document_elements,
            }
            return json.dumps(message)

        return chat.llm_raw_response
