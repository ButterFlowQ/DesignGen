from typing import List

from agents.types import AgentType, LLMMessage, LLMResponse
from workflowManager.models.models import ChatMessage

from .agent_interface import AgentInterface
from .helper import get_message_content


class APIContractAgent(AgentInterface):
    """
    An agent responsible for defining API contracts and interactions in a system design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the APIContractAgent with a system message and response format.
        """
        system_message = (
            "You are an API Contracts and Interaction Agent in a system design pipeline. Your role is to:\n"
            "    1. Define and specify API contracts between system components\n"
            "    2. Design interaction protocols for internal and external communications\n"
            "    3. Ensure APIs adhere to industry standards and best practices\n"
            "    4. Identify and resolve potential integration issues\n"
            "    5. Maintain documentation for all API endpoints and interaction flows\n\n"
            "You will receive a user message and the current state of the complete design document "
            "in the following JSON format:\n\n"
            "{\n"
            '  "document": {\n'
            '      "functional_requirements": [...],\n'
            '      "non_functional_requirements": [...],\n'
            '      "architecture": {...},\n'
            '      "api_contracts": [\n'
            '          "Current API contract 1",\n'
            '          "Current API contract 2"\n'
            "      ]\n"
            "  },\n"
            '  "user_message": "User\'s input or request regarding API contracts"\n'
            "}\n\n"
            "For each interaction, you must provide a response in the following JSON format:\n\n"
            "{\n"
            "  'api_contracts': [\n"
            "      'Detailed API contract description 1',\n"
            "      'Detailed API contract description 2'\n"
            "  ],\n"
            "  'communication': 'Explanation of changes or reasoning',\n"
            "  'ready_for_next_workflow': boolean\n"
            "}\n\n"
            "Example:\n"
            "{\n"
            "  'api_contracts': [\n"
            "      'GET /users - Retrieves a list of users',\n"
            "      'POST /users - Creates a new user with email and password'\n"
            "  ],\n"
            "  'communication': "
            "'Added POST /users endpoint to support user registration',\n"
            "  'ready_for_next_workflow': false\n"
            "}\n"
        )

        response_format = {
            "updated_workflow_doc": "api_contracts",
            "response_message": "communication",
            "move_to_next_workflow": "ready_for_next_workflow",
        }
        super().__init__(AgentType.API_CONTRACT, system_message, response_format)

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the chat history and generates a response.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the updated API contracts, communication, and workflow status.
        """
        llm_messages = self.generate_llm_history(chat_history)
        return self.llm.get_response(llm_messages, self.response_format)

    def generate_llm_history(self, chat_history: List[ChatMessage]) -> List[LLMMessage]:
        """
        Converts the chat history into LLM-compatible messages.

        :param chat_history: The history of chat messages to transform.
        :return: A list of LLMMessage dictionaries.
        """
        llm_messages: List[LLMMessage] = []
        llm_messages.append({"role": "system", "content": self.system_message})

        for chat in chat_history:
            is_api_agent = chat.from_agent_type == AgentType.API_CONTRACT.value
            is_user_agent = chat.from_agent_type == AgentType.USER.value

            role = "assistant" if is_api_agent else "user"
            message_content = get_message_content(chat, is_user_agent)
            llm_messages.append({"role": role, "content": message_content})

        return llm_messages 