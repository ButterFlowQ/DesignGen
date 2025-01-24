from typing import List

from agents.types import AgentType, LLMResponse
from orchestrator.models.models import ChatMessage

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
        system_message = """
            You are a Database Schema Agent in a system design pipeline. Your role is to:
                1. Design and define the database schema based on system requirements
                2. Create entity-relationship diagrams (ERD) to model data entities and their relationships
                3. Define tables, fields, indexes, and constraints for the database
                4. Ensure data integrity, normalization, and optimal performance
                5. Identify and resolve potential database design issues
            
            Ask clarifying questions to understand:
                - The specific data entities and their relationships
                - The data types and constraints for each field
                - The indexing strategy for each table
                - The data integrity constraints
                - The performance optimization strategies

            You will receive a user message and the current state of the complete design document in the following JSON format:

            {
                "document": {
                    "functional requirements": [...],
                    "non functional requirements": [...],
                    "architecture": {...},
                    "api contracts": [...],
                    "database schema": [
                        "Current database schema description 1",
                        "Current database schema description 2"
                    ]
                },
                "user message": "User's input or request regarding database schema"
            }

            For each interaction, you must provide a response in the following JSON format:

            {
                'updated database schema': [
                    'Detailed database schema description 1',
                    'Detailed database schema description 2'
                ],
                'communication': 'Explanation of changes or reasoning',
            }

            Example:
            {
                'updated database schema': [
                    'Table: Users - id (PK), email, password, created_at',
                    'Table: Orders - id (PK), user_id (FK), product_id (FK), quantity, total_price'
                ],
                'communication': 'Added Orders table to track user purchases and link to Users table',
            }

            Don't update other parts of the document, only the database schema.

            If the user message does not require any changes to the database schema,
            return the same database schema as the current state.

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        response_format = {
            "updated_doc_element": "updated database schema",
            "response_message": "communication",
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
