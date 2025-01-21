from typing import List

from agents.types import AgentType, LLMMessage, LLMResponse
from workflowManager.models.models import ChatMessage

from .agent_interface import AgentInterface
from .helper import get_message_content


class FunctionalRequirementAgent(AgentInterface):
    """
    An agent responsible for handling and refining functional requirements in a system design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the FunctionalRequirementAgent with a system message and a specified response format.
        """
        system_message = """
            You are a Functional requirements agent in a system design pipeline. Your role is to:
                1. Gather and analyze functional requirements from user inputs
                2. Refine and detail functional requirements for clarity and completeness
                3. Ensure that functional requirements are specific, measurable, and achievable
                4. Identify dependencies and relationships between functional requirements
                5. Detect and flag any inconsistencies or ambiguities in functional requirements

            Ask clarifying questions to understand:
                - The specific actions users should be able to perform
                - Expected system behaviors and responses
                - Data inputs, outputs and validations needed
                - Business rules and constraints
                - User roles and permissions
                - Integration requirements with other systems
            
            Make sure all the ambuguities are resolve before setting ready_for_next_workflow to true.

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
                'functional_requirements': [
                    'Detailed functional requirement description 1',
                    'Detailed functional requirement description 2'
                ],
                'communication': 'Explanation of changes. Or clarification question to the user.',
                'ready_for_next_workflow': boolean indicating if all functional requirements have been finalized (true) or still need discussion (false)
            }

            Example:
            {
                'functional_requirements': [
                    'Users must be able to register for an account',
                    'Users must be able to authenticate using email and password'
                ],
                'communication': 'Refined registration process to include email verification',
                'ready_for_next_workflow': false
            }
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_workflow_doc": "functional_requirements",
            "response_message": "communication",
            "move_to_next_workflow": "ready_for_next_workflow",
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
            # Compare the enum's value to the stored string
            is_functional_requirement_agent = chat.from_agent_type == AgentType.FUNCTIONAL_REQUIREMENT.value
            is_user_agent = chat.from_agent_type == AgentType.USER.value

            role = "assistant" if is_functional_requirement_agent else "user"
            message_content = get_message_content(chat, is_user_agent)
            llm_messages.append({"role": role, "content": message_content})

        return llm_messages
