from typing import List

from agents.types import AgentType, LLMMessage, LLMResponse
from workflowManager.models.models import ChatMessage

from .agent_interface import AgentInterface
from .helper import get_message_content


class PerformanceOptimizationAgent(AgentInterface):
    """
    An agent responsible for performance optimization recommendations.
    """

    def __init__(self) -> None:
        """
        Initializes the PerformanceOptimizationAgent with a system message and response format.
        """
        system_message = (
            "You are a Performance Optimization Agent in a system design pipeline. Your role is to:\n"
            "    1. Analyze system design for performance bottlenecks and scalability issues\n"
            "    2. Propose optimization strategies to enhance system performance and scalability\n"
            "    3. Implement caching, load balancing, and other performance improvement techniques\n"
            "    4. Evaluate the impact of proposed optimizations on overall system design\n"
            "    5. Ensure that performance requirements are met and aligned with non-functional requirements\n\n"
            "You will receive a user message and the current state of the complete design document "
            "in the following JSON format:\n\n"
            "{\n"
            '  "document": {\n'
            '      "functional_requirements": [...],\n'
            '      "non_functional_requirements": [...],\n'
            '      "architecture": {...},\n'
            '      "api_contracts": [...],\n'
            '      "database_schema": [...],\n'
            '      "performance_optimizations": [\n'
            '          "Current performance metric 1",\n'
            '          "Current performance metric 2"\n'
            "      ]\n"
            "  },\n"
            '  "user_message": "User\'s input or request regarding performance optimization"\n'
            "}\n\n"
            "For each interaction, you must provide a response in the following JSON format:\n\n"
            "{\n"
            "  'performance_optimizations': [\n"
            "      'Detailed performance metric description 1',\n"
            "      'Detailed performance metric description 2'\n"
            "  ],\n"
            "  'communication': 'Explanation of changes or reasoning',\n"
            "  'ready_for_next_workflow': boolean\n"
            "}\n\n"
            "Example:\n"
            "{\n"
            "  'performance_optimizations': [\n"
            "      'Implemented Redis caching to reduce database load by 30%',\n"
            "      'Configured load balancer to distribute traffic across three servers'\n"
            "  ],\n"
            "  'communication': "
            "'Added Redis caching to improve response times and configured load balancer for better scalability',\n"
            "  'ready_for_next_workflow': false\n"
            "}\n"
        )

        response_format = {
            "updated_workflow_doc": "performance_optimizations",
            "response_message": "communication",
            "move_to_next_workflow": "ready_for_next_workflow",
        }
        super().__init__(AgentType.PERFORMANCE_OPTIMIZATION, system_message, response_format)

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the chat history and generates a response.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the updated performance optimizations, communication, and workflow status.
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
            is_perf_agent = chat.from_agent_type == AgentType.PERFORMANCE_OPTIMIZATION.value
            is_user_agent = chat.from_agent_type == AgentType.USER.value

            role = "assistant" if is_perf_agent else "user"
            message_content = get_message_content(chat, is_user_agent, "performance_optimizations")
            llm_messages.append({"role": role, "content": message_content})

        return llm_messages 