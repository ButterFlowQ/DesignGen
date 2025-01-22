from typing import List

from agents.types import AgentType, LLMMessage, LLMResponse
from workflowManager.models.models import ChatMessage

from .agent_interface import AgentInterface
from ..helper import get_message_content


class FunctionalRequirementAgent(AgentInterface):
    """
    An agent responsible for handling and refining functional requirements in a system design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the FunctionalRequirementAgent with a system message and a specified response format.
        """
        system_message = (
            "You are a Functional requirements agent in a system design pipeline. Your role is to:\n"
            "    1. Gather and analyze functional requirements from user inputs\n"
            "    2. Refine and detail functional requirements for clarity and completeness\n"
            "    3. Ensure that functional requirements are specific, measurable, and achievable\n"
            "    4. Identify dependencies and relationships between functional requirements\n"
            "    5. Detect and flag any inconsistencies or ambiguities in functional requirements\n\n"
            "You will receive a user message and the current state of the complete design document "
            "in the following JSON format:\n\n"
            "{\n"
            '  "document": {\n'
            '      "functional_requirements": [\n'
            '          "Current functional requirement 1",\n'
            '          "Current functional requirement 2"\n'
            "      ],\n"
            '      "non_functional_requirements": [\n'
            '          "Current non-functional requirement 1",\n'
            '          "Current non-functional requirement 2"\n'
            "      ],\n"
            '      "architecture": {}\n'
            "  },\n"
            '  "user_message": "User\'s input message or requirement"\n'
            "}\n\n"
            "For each interaction, you must provide a response in the following JSON format:\n\n"
            "{\n"
            "  'functional_requirements': [\n"
            "      'Detailed functional requirement description 1',\n"
            "      'Detailed functional requirement description 2'\n"
            "  ],\n"
            "  'communication': 'Explanation of changes or reasoning',\n"
            "  'ready_for_next_workflow': boolean\n"
            "}\n\n"
            "Example:\n"
            "{\n"
            "  'functional_requirements': [\n"
            "      'Users must be able to register for an account',\n"
            "      'Users must be able to authenticate using email and password'\n"
            "  ],\n"
            "  'communication': "
            "'Refined registration process to include email verification',\n"
            "  'ready_for_next_workflow': false\n"
            "}\n"
        )

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_workflow_doc": "functional_requirements",
            "response_message": "communication",
        }
        super().__init__(AgentType.FUNCTIONAL_REQUIREMENT, system_message, response_format)

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the given chat history by generating LLM messages and querying the LLM for a
        structured response.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the updated requirements, communication, and a boolean
                 indicating whether to move to the next workflow.
        """
        llm_messages = self.generate_llm_history(chat_history)
        return self.llm.get_response(llm_messages, self.response_format)

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
            message_content = get_message_content(chat)
            llm_messages.append({"role": role, "content": message_content})

        return llm_messages
