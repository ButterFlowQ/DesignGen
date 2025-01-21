from typing import List

from agents.types import AgentType, LLMMessage, LLMResponse
from workflowManager.models.models import ChatMessage

from .agent_interface import AgentInterface
from .helper import get_message_content


class NonFunctionalRequirementAgent(AgentInterface):
    """
    An agent responsible for handling non-functional requirements in a system design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the NonFunctionalRequirementAgent with a system message and response format.
        """
        system_message = """
            You are a Non-Functional Requirements Agent in a system design pipeline. Your role is to:
                1. Gather and analyze non-functional requirements from user inputs
                2. Refine and detail non-functional requirements for clarity and completeness
                3. Ensure that non-functional requirements are specific, measurable, and achievable
                4. Identify dependencies and relationships between non-functional requirements
                5. Detect and flag any inconsistencies or ambiguities in non-functional requirements

            You will receive a user message and the current state of the complete design document in the following JSON format:

            {
                "document": {
                    "functional_requirements": [
                        "Current functional requirement 1",
                        "Current functional requirement 2"
                    ],
                    "non_functional_requirements": [
                        "Current non-functional requirement 1",
                        "Current non-functional requirement 2"
                    ],
                    "architecture": {}
                },
                "user_message": "User's input message or requirement"
            }

            For each interaction, you must provide a response in the following JSON format:

            {
                'non_functional_requirements': [
                    'Detailed non-functional requirement description 1',
                    'Detailed non-functional requirement description 2'
                ],
                'communication': 'Explanation of changes or reasoning',
                'ready_for_next_workflow': boolean
            }

            Example:
            {
                'non_functional_requirements': [
                    'System must handle 10,000 concurrent users',
                    'System must ensure data encryption in transit and at rest'
                ],
                'communication': 'Updated concurrency requirement to 10,000 users based on projected growth',
                'ready_for_next_workflow': false
            }
        """
    

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

    def generate_llm_history(self, chat_history: List[ChatMessage]) -> List[LLMMessage]:
        """
        Converts the chat history into LLM-compatible messages.

        :param chat_history: The history of chat messages to transform.
        :return: A list of LLMMessage dictionaries.
        """
        llm_messages: List[LLMMessage] = []
        llm_messages.append({"role": "system", "content": self.system_message})

        for chat in chat_history:
            is_nfr_agent = chat.from_agent_type == AgentType.NON_FUNCTIONAL_REQUIREMENT.value
            is_user_agent = chat.from_agent_type == AgentType.USER.value

            role = "assistant" if is_nfr_agent else "user"
            message_content = get_message_content(chat, is_user_agent)
            llm_messages.append({"role": role, "content": message_content})

        return llm_messages 