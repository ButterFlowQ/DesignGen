from typing import List

from agents.types import AgentType, LLMMessage, LLMResponse
from workflowManager.models.models import ChatMessage

from .agent_interface import AgentInterface


class RequirementAgent(AgentInterface):
    """
    An agent responsible for handling and refining requirements in a system design pipeline.

    Responsibilities include:
      1. Analyzing and refining incoming requirements
      2. Maintaining consistency across all requirements
      3. Identifying missing critical requirements
      4. Flagging potential conflicts or ambiguities
      5. Ensuring requirements are specific, measurable, and achievable
    """

    def __init__(self) -> None:
        """
        Initializes the RequirementAgent with a system message and a specified response format.
        """
        system_message = (
            "You are a Requirements Analysis Agent in a system design pipeline. Your role is to:\n"
            "    1. Analyze and refine incoming requirements\n"
            "    2. Maintain consistency across all requirements\n"
            "    3. Identify missing critical requirements\n"
            "    4. Flag potential conflicts or ambiguities\n"
            "    5. Ensure requirements are specific, measurable, and achievable\n\n"
            "You will receive a user message and the current state of the complete design document "
            "in the following JSON format:\n\n"
            "{\n"
            '  "document": {\n'
            '      "requirements": [\n'
            '          "Current requirement 1",\n'
            '          "Current requirement 2"\n'
            "      ],\n"
            '      "architecture": {}\n'
            "  },\n"
            '  "user_message": "User\'s input message or requirement"\n'
            "}\n\n"
            "For each interaction, you must provide a response in the following JSON format:\n\n"
            "{\n"
            "  'requirements': [\n"
            "      'Detailed requirement description 1',\n"
            "      'Detailed requirement description 2'\n"
            "  ],\n"
            "  'communication': 'Explanation of changes or reasoning',\n"
            "  'ready_for_next_workflow': boolean\n"
            "}\n\n"
            "Example:\n"
            "{\n"
            "  'requirements': [\n"
            "      'Users must be able to register for an account',\n"
            "      'Users must be able to authenticate using email and password'\n"
            "  ],\n"
            "  'communication': "
            "'Updated authentication requirement to specify password complexity',\n"
            "  'ready_for_next_workflow': false\n"
            "}\n"
        )

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_workflow_doc": "requirements",
            "response_message": "communication",
            "move_to_next_workflow": "ready_for_next_workflow",
        }
        super().__init__(AgentType.REQUIREMENT, system_message, response_format)

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
            # Compare the enum's value to the stored string
            is_requirement_agent = chat.from_agent_type == AgentType.REQUIREMENT.value
            is_user_agent = chat.from_agent_type == AgentType.USER.value

            role = "assistant" if is_requirement_agent else "user"
            message_content = self.get_message_content(chat, is_user_agent)
            llm_messages.append({"role": role, "content": message_content})

        return llm_messages

    def get_message_content(self, chat: ChatMessage, is_user_agent: bool) -> str:
        """
        Builds the appropriate message content depending on whether the sender is a user or
        the RequirementAgent.

        :param chat: The ChatMessage being processed.
        :param is_user_agent: True if the sender is the user, False otherwise.
        :return: A string containing the relevant content for the LLM.
        """
        if is_user_agent:
            # Retrieve the relevant document (if it exists)
            if chat.document:
                document_text = self.get_relevant_document(chat.document)
            else:
                document_text = "No document available."

            return (
                f"{chat.message}\n\n"
                "Update the requirements in the doc given below as desired:\n"
                f"Document:\n{document_text}"
            )
        return chat.message

    def get_relevant_document(self, document) -> str:
        """
        Returns a string representation of the given document. If you need more complex
        behavior (e.g., extracting only 'requirements'), adapt this method accordingly.

        :param document: The Document object or a related entity from ChatMessage.
        :return: A string representing the document content.
        """
        # In a real scenario, you might extract JSON fields or return a summary. For now, we
        # assume the document has a suitable string conversion or a specific field to display.
        return str(document)
