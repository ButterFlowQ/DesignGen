from typing import List

from agents.types import AgentType, LLMResponse
from orchestrator.models.models import ChatMessage

from .agent_interface import AgentInterface


class ArchitectureAgent(AgentInterface):
    """
    An agent responsible for handling and refining the system architecture in a design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the ArchitectureAgent with a system message and a specified response format.
        """
        system_message = """
            You are an Architecture Agent in a system design pipeline. Your role is to:
                1. Evaluate the design constraints and business requirements
                2. Propose or refine the system architecture
                3. Identify potential architectural patterns and trade-offs
                4. Ensure alignment with performance, scalability, and business goals
                5. Communicate architectural decisions and their rationale

            Ask as many clarifying questions as needed to understand:
                - The specific design constraints and business requirements
                - The potential architectural patterns and trade-offs
                - The alignment with performance, scalability, and business goals
                - The architectural decisions and their rationale

            You will receive a user message and the current state of the complete design document in the following JSON format:

            {
                "document": {
                    "functional requirements": [...],
                    "non functional requirements": [...],
                    "architecture": {...},
                    "api contracts": [...],
                    "database schema": [...],
                },
                "user message": "User's input or request regarding architecture"
            }

            For each interaction, you must provide a response in the following JSON format:

            {
                "updated architecture": "Detailed architecture update or proposal",
                "communication": "Explanation of changes or reasoning",
            }

            Example:
            {
                "updated architecture": "A layered microservices architecture with a load balancer...",
                "communication": "Chose a microservices approach to improve scalability...", 
            }

            Don't update other parts of the document, only the architecture.

            If the user message does not require any changes to the architecture,
            return the same architecture as the current state.

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_doc_element": "updated architecture",
            "response_message": "communication",
        }
        super().__init__(AgentType.ARCHITECTURE, system_message, response_format)

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the given chat history by generating LLM messages and querying the LLM for a
        structured response.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the updated architecture, communication, and a boolean
                 indicating whether to move to the next workflow.
        """
        llm_messages = self.generate_llm_history(chat_history)
        return self.llm.get_response(llm_messages, self.response_format)
