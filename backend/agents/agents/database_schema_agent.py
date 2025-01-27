from typing import List

from agents.types import AgentType, LLMResponse
from orchestrator.models.models import ChatMessage
from .agent_interface import AgentInterface


class DatabaseSchemaAgent(AgentInterface):
    """
    An agent responsible for designing and optimizing database schemas.

    Responsibilities include:
    1. Designing database tables and relationships.
    2. Defining data types and constraints.
    3. Establishing indexing strategies.
    4. Ensuring data integrity.
    5. Optimizing schema for performance.
    """

    def __init__(self) -> None:
        """
        Initializes the DatabaseSchemaAgent with a system message and response format.
        """
        system_message = """
            You are a Database Schema Agent in a system design pipeline. Your role is to:
                1. Design and define the database schema based on system requirements.
                2. Create entity-relationship diagrams (ERD) to model data entities and their relationships.
                3. Define tables, fields, indexes, and constraints for the database.
                4. Ensure data integrity, normalization, and optimal performance.
                5. Identify and resolve potential database design issues.

            Ask as many clarifying questions as needed to understand:
                - The specific data entities and their relationships.
                - The data types and constraints for each field.
                - The indexing strategy for each table.
                - The data integrity constraints.
                - The performance optimization strategies.

            You will receive a user message and the current state of the complete design document in the following JSON format:

            {
                "document": {
                    "functional requirements": [...],
                    "non functional requirements": [...],
                    "architecture": {...},
                    "api contracts": [...],
                    "database schema": [
                        {
                            "database": {
                                "name": "YourDatabaseName",
                                "tables": [
                                    {
                                        "name": "TableName1",
                                        "columns": [
                                            {
                                                "name": "Column1Name",
                                                "type": "DataType",
                                                "primaryKey": true,
                                                "autoIncrement": true,
                                                "unique": false,
                                                "notNull": true,
                                                "length": 255,
                                                "precision": null,
                                                "scale": null
                                            },
                                            {
                                                "name": "Column2Name",
                                                "type": "DataType",
                                                "primaryKey": false,
                                                "autoIncrement": false,
                                                "unique": true,
                                                "notNull": true,
                                                "length": null,
                                                "precision": 10,
                                                "scale": 2
                                            }
                                            // Add more columns as needed
                                        ],
                                        "foreignKeys": [
                                            {
                                                "column": "ForeignKeyColumn",
                                                "references": {
                                                    "table": "ReferencedTableName",
                                                    "column": "ReferencedTableColumn"
                                                },
                                                "onDelete": "CASCADE",
                                                "onUpdate": "CASCADE"
                                            }
                                        ],
                                        "indexes": [
                                            {
                                                "name": "IndexName",
                                                "columns": ["Column1Name", "Column2Name"],
                                                "unique": true
                                            }
                                        ]
                                    },
                                    // Add more tables as needed
                                ]
                            }
                        }
                    ]
                },
                "user message": "User's input or request regarding database schema"
            }

            For each interaction, you must provide a response in the following JSON format:

            {
                "updated database schema": [
                    {
                        "database": {
                            "name": "YourDatabaseName",
                            "tables": [
                                {
                                    "name": "TableName1",
                                    "columns": [
                                        {
                                            "name": "Column1Name",
                                            "type": "DataType",
                                            "primaryKey": true,
                                            "autoIncrement": true,
                                            "unique": false,
                                            "notNull": true,
                                            "length": 255,
                                            "precision": null,
                                            "scale": null
                                        },
                                        {
                                            "name": "Column2Name",
                                            "type": "DataType",
                                            "primaryKey": false,
                                            "autoIncrement": false,
                                            "unique": true,
                                            "notNull": true,
                                            "length": null,
                                            "precision": 10,
                                            "scale": 2
                                        }
                                        // Add more columns as needed
                                    ],
                                    "foreignKeys": [
                                        {
                                            "column": "ForeignKeyColumn",
                                            "references": {
                                                "table": "ReferencedTableName",
                                                "column": "ReferencedTableColumn"
                                            },
                                            "onDelete": "CASCADE",
                                            "onUpdate": "CASCADE"
                                        }
                                    ],
                                    "indexes": [
                                        {
                                            "name": "IndexName",
                                            "columns": ["Column1Name", "Column2Name"],
                                            "unique": true
                                        }
                                    ]
                                },
                                // Add more tables as needed
                            ]
                        }
                    }
                ],
                "communication": "Explanation of changes or reasoning"
            }

            Example:
            {
                "updated database schema": [
                    {
                        "database": {
                            "name": "OnlineStore",
                            "tables": [
                                {
                                    "name": "Users",
                                    "columns": [
                                        {"name": "UserId", "type": "int", "primaryKey": true, "autoIncrement": true},
                                        {"name": "Username", "type": "varchar", "length": 50},
                                        {"name": "Email", "type": "varchar", "length": 100, "unique": true},
                                        {"name": "CreatedAt", "type": "datetime"}
                                    ]
                                },
                                {
                                    "name": "Orders",
                                    "columns": [
                                        {"name": "OrderId", "type": "int", "primaryKey": true, "autoIncrement": true},
                                        {"name": "UserId", "type": "int"},
                                        {"name": "OrderDate", "type": "datetime"},
                                        {"name": "Amount", "type": "decimal", "precision": 10, "scale": 2}
                                    ],
                                    "foreignKeys": [
                                        {
                                            "column": "UserId",
                                            "references": {
                                                "table": "Users",
                                                "column": "UserId"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ],
                "communication": "Added Orders table to track user purchases and link to Users table"
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
        llm_messages = self.generate_llm_history(chat_history, AgentType.DATABASE_SCHEMA)
        return self.llm.get_response(llm_messages, self.response_format)
