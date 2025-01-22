from typing import List

from agents.types import AgentType, LLMResponse
from workflowManager.models.models import ChatMessage

from .agent_interface import AgentInterface


class NonFunctionalRequirementAgent(AgentInterface):
    """
    An agent responsible for handling non-functional requirements in a system design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the NonFunctionalRequirementAgent with a system message and response format.
        """
        system_message = (
            "You are a Non-Functional Requirements Agent in a system design pipeline. Your role is to:\n"
            "    1. Gather and analyze non-functional requirements from user inputs\n"
            "    2. Refine and detail non-functional requirements for clarity and completeness\n"
            "    3. Ensure that non-functional requirements are specific, measurable, and achievable\n"
            "    4. Identify dependencies and relationships between non-functional requirements\n"
            "    5. Detect and flag any inconsistencies or ambiguities in non-functional requirements\n\n"
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
            "  'non_functional_requirements': [\n"
            "      'Detailed non-functional requirement description 1',\n"
            "      'Detailed non-functional requirement description 2'\n"
            "  ],\n"
            "  'communication': 'Explanation of changes or reasoning',\n"
            "  'ready_for_next_workflow': boolean\n"
            "}\n\n"
            "Example:\n"
            "{\n"
            "  'non_functional_requirements': [\n"
            "      'System must handle 10,000 concurrent users',\n"
            "      'System must ensure data encryption in transit and at rest'\n"
            "  ],\n"
            "  'communication': "
            "'Updated concurrency requirement to 10,000 users based on projected growth',\n"
            "  'ready_for_next_workflow': false\n"
            "}\n"
        )

        response_format = {
            "updated_workflow_doc": "non_functional_requirements",
            "response_message": "communication",
            "move_to_next_workflow": "ready_for_next_workflow",
        }
        super().__init__(AgentType.NON_FUNCTIONAL_REQUIREMENT, system_message, response_format)

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the chat history and generates a response.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the updated NFRs, communication, and workflow status.
        """
        llm_messages = self.generate_llm_history(chat_history)
        return self.llm.get_response(llm_messages, self.response_format)