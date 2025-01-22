from typing import List

from agents.types import AgentType, LLMResponse
from workflowManager.models.models import ChatMessage

from .agent_interface import AgentInterface


class DatabaseSchemaAgent(AgentInterface):
    """
    An agent responsible for designing and optimizing database schemas.

    Responsibilities include:
    1. Designing database tables and relationships
    2. Defining data types and constraints
    3. Establishing indexing strategies
    4. Ensuring data integrity
    5. Optimizing schema for performance
    """

    def __init__(self) -> None:
        """
        Initializes the DatabaseSchemaAgent with a system message and response format.
        """
        system_message = (
            "You are a Database Schema Agent in a system design pipeline. Your role is to:\n"
            "    1. Design and define the database schema based on system requirements\n"
            "    2. Create entity-relationship diagrams (ERD) to model data entities and their relationships\n"
            "    3. Define tables, fields, indexes, and constraints for the database\n"
            "    4. Ensure data integrity, normalization, and optimal performance\n"
            "    5. Identify and resolve potential database design issues\n\n"
            "You will receive a user message and the current state of the complete design document "
            "in the following JSON format:\n\n"
            "{\n"
            '  "document": {\n'
            '      "functional_requirements": [...],\n'
            '      "non_functional_requirements": [...],\n'
            '      "architecture": {...},\n'
            '      "api_contracts": [...],\n'
            '      "database_schema": [\n'
            '          "Current database schema description 1",\n'
            '          "Current database schema description 2"\n'
            "      ]\n"
            "  },\n"
            '  "user_message": "User\'s input or request regarding database schema"\n'
            "}\n\n"
            "For each interaction, you must provide a response in the following JSON format:\n\n"
            "{\n"
            "  'database_schema': [\n"
            "      'Detailed database schema description 1',\n"
            "      'Detailed database schema description 2'\n"
            "  ],\n"
            "  'communication': 'Explanation of changes or reasoning',\n"
            "  'ready_for_next_workflow': boolean\n"
            "}\n\n"
            "Example:\n"
            "{\n"
            "  'database_schema': [\n"
            "      'Table: Users - id (PK), email, password, created_at',\n"
            "      'Table: Orders - id (PK), user_id (FK), product_id (FK), quantity, total_price'\n"
            "  ],\n"
            "  'communication': "
            "'Added Orders table to track user purchases and link to Users table',\n"
            "  'ready_for_next_workflow': false\n"
            "}\n"
        )

        response_format = {
            "updated_workflow_doc": "database_schema",
            "response_message": "communication",
            "move_to_next_workflow": "ready_for_next_workflow",
        }
        super().__init__(AgentType.DATABASE_SCHEMA, system_message, response_format)

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the chat history and generates a response.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the updated database schema, communication, and workflow status.
        """
        llm_messages = self.generate_llm_history(chat_history)
        return self.llm.get_response(llm_messages, self.response_format)