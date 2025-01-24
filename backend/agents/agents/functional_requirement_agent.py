from typing import List

from agents.types import AgentType, LLMResponse
from orchestrator.models.models import ChatMessage

from .agent_interface import AgentInterface


class FunctionalRequirementAgent(AgentInterface):
    """
    An agent responsible for handling and refining functional requirements in a system design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the Functional requirement agent with a system message and a specified response format.
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
            
            You will receive a user message and the current state of the complete design document in the following JSON format:
            {
                "document": {
                    "functional requirements": [
                        "Current functional requirement 1",
                        "Current functional requirement 2"
                    ],
                    "non functional requirements": [
                        "Current non-functional requirement 1",
                        "Current non-functional requirement 2",
                    ],
                    "architecture": {},
                    "api contract": {},
                    "database schema": {},
                },
                "user message": "User's input message or requirement"
            }
            For each interaction, you must provide a response in the following JSON format:
            {
                "updated functional requirements": [
                    "Detailed functional requirement description 1",
                    "Detailed functional requirement description 2"
                ],
                "communication": "Explanation of changes. Or clarification question to the user."
            }
            Example:
            {
                "updated functional requirements": [
                    "Users must be able to register for an account",
                    "Users must be able to authenticate using email and password"
                ],
                "communication": "Refined registration process to include email verification"
            }

            Don't update other parts of the document, only the functional requirements.

            If the user message does not require any changes to the functional requirements,
            return the same functional requirements as the current state.

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_doc_element": "updated functional requirements",
            "response_message": "communication",
        }
        super().__init__(
            AgentType.FUNCTIONAL_REQUIREMENT, system_message, response_format
        )

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
