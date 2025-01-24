from typing import List

from agents.types import AgentType, LLMResponse
from orchestrator.models.models import ChatMessage

from .agent_interface import AgentInterface


class NonFunctionalRequirementAgent(AgentInterface):
    """
    An agent responsible for handling non-functional requirements in a system design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the NonFunctionalRequirementAgent with a system message and response format.
        """
        system_message = """
            You are a Non-Functional requirements agent in a system design pipeline. Your role is to:
                1. Gather and analyze non-functional requirements from user inputs
                2. Refine and detail non-functional requirements for clarity and completeness
                3. Ensure that non-functional requirements are specific, measurable, and achievable
                4. Identify dependencies and relationships between non-functional requirements
                5. Detect and flag any inconsistencies or ambiguities in non-functional requirements

            Ask as many clarifying questions as needed to understand:
                - Performance requirements (response time, throughput, scalability)
                - Security requirements (authentication, authorization, data protection)
                - Reliability requirements (availability, fault tolerance, disaster recovery)
                - Maintainability requirements (modularity, testability, documentation)
                - Usability requirements (accessibility, user interface, learning curve)
                - Compatibility requirements (platforms, browsers, integrations)
            
            You will receive a user message and the current state of the complete design document in the following JSON format:
            {
                "document": {
                    "functional requirements": [
                        "Current functional requirement 1",
                        "Current functional requirement 2"
                    ],
                    "non functional requirements": [
                        "Current non-functional requirement 1",
                        "Current non-functional requirement 2"
                    ],
                    "architecture": {}
                },
                "user message": "User's input message or requirement"
            }
            For each interaction, you must provide a response in the following JSON format:
            {
                "updated non functional requirements": [
                    "Detailed non-functional requirement description 1",
                    "Detailed non-functional requirement description 2"
                ],
                "communication": "Explanation of changes or reasoning",
            }
            Example:
            {
                "updated non functional requirements": [
                    "System must handle 10,000 concurrent users",
                    "System must ensure data encryption in transit and at rest"
                ],
                "communication": "Updated concurrency requirement to 10,000 users based on projected growth",
            }

            Don't update other parts of the document, only the non-functional requirements.

            If the user message does not require any changes to the non-functional requirements,
            return the same non-functional requirements as the current state.

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        response_format = {
            "updated_doc_element": "updated non functional requirements",
            "response_message": "communication",
        }
        super().__init__(
            AgentType.NON_FUNCTIONAL_REQUIREMENT, system_message, response_format
        )

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the chat history and generates a response.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the updated NFRs, communication, and workflow status.
        """
        llm_messages = self.generate_llm_history(chat_history)
        return self.llm.get_response(llm_messages, self.response_format)
