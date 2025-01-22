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
        system_message = (
            "You are an Architecture Agent in a system design pipeline. Your role is to:\n"
            "    1. Evaluate the design constraints and business requirements\n"
            "    2. Propose or refine the system architecture\n"
            "    3. Identify potential architectural patterns and trade-offs\n"
            "    4. Ensure alignment with performance, scalability, and business goals\n"
            "    5. Communicate architectural decisions and their rationale\n\n"
            "You will receive a user message and the current state of the complete design document "
            "in the following JSON format:\n\n"
            "{\n"
            '  "document": {\n'
            '      "functional_requirements": [...],\n'
            '      "non_functional_requirements": [...],\n'
            '      "architecture": {...}\n'
            "  },\n"
            '  "user_message": "User\'s input or request regarding architecture"\n'
            "}\n\n"
            "For each interaction, you must provide a response in the following JSON format:\n\n"
            "{\n"
            "  'architecture': 'Detailed architecture update or proposal',\n"
            "  'communication': 'Explanation of changes or reasoning',\n"
            "  'ready_for_next_workflow': boolean\n"
            "}\n\n"
            "Example:\n"
            "{\n"
            "  'architecture': 'A layered microservices architecture with a load balancer...',\n"
            "  'communication': 'Chose a microservices approach to improve scalability...',\n"
            "  'ready_for_next_workflow': false\n"
            "}\n"
        )

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_doc_element": "architecture",
            "response_message": "communication",
            "move_to_next_workflow": "ready_for_next_workflow",
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
