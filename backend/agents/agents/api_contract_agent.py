from typing import List

from agents.types import AgentType, LLMResponse
from orchestrator.models.models import ChatMessage
from .agent_interface import AgentInterface


class APIContractAgent(AgentInterface):
    """
    An agent responsible for defining API contracts and interactions in a system design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the APIContractAgent with a system message and response format.
        """
        system_message = """
            You are an API Contracts and Interaction Agent in a system design pipeline. Your role is to:
                1. Define and specify API contracts between system components.
                2. Design interaction protocols for internal and external communications.
                3. Ensure APIs adhere to industry standards and best practices.
                4. Identify and resolve potential integration issues.
                5. Maintain documentation for all API endpoints and interaction flows.
                6. Return the API contracts in Swagger API JSON format.

            Ask as many clarifying questions as needed to understand:
                - The required API endpoints and their purposes.
                - The request/response formats and data structures.
                - The authentication and authorization requirements.
                - The error handling and status codes.
                - The API versioning and backward compatibility needs.

            You will receive a user message and the current state of the complete design document in the following JSON format:

            {
              "document": {
                  "functional requirements": [...],
                  "non functional requirements": [...],
                  "architecture": {...},
                  "api contracts": [
                        {
                        "swagger": "2.0",
                        "info": {
                            "title": "",
                            "version": ""
                        },
                        "paths": {
                            "<path>": {
                                "get": {
                                    "summary": "",
                                    "parameters": [
                                        {
                                            ...
                                        }
                                    ],
                                    "responses": {
                                        "200": {
                                            "description": "Successful response",
                                            "schema": {
                                                "type": "object",
                                                "properties": {
                                                    "name": { "type": "string" },
                                                    "email": { "type": "string" }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                  ],
                  "database schema": [...],
              },
              "user message": "User's input or request regarding API contracts"
            }

            For each interaction, you must provide a response in the following JSON format:

            {
              "updated api contracts": [
                  {
                    "swagger": "2.0",
                    "info": {
                        "title": "",
                        "version": ""
                    },
                    "paths": {
                        "<path>": {
                            "get": {
                                "summary": "",
                                "parameters": [
                                    {
                                        ...
                                    }
                                ],
                                "responses": {
                                    "200": {
                                        "description": "Successful response",
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "name": { "type": "string" },
                                                "email": { "type": "string" }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                  }
              ],
              "communication": "Explanation of changes or reasoning",
            }

            Example:
            {
              "updated api contracts": [
                    {
                    "swagger": "2.0",
                    "info": {
                        "title": "Example API",
                        "version": "1.0"
                    },
                    "paths": {
                        "/users/{userId}": {
                        "get": {
                            "summary": "Get user by ID",
                            "parameters": [
                                {
                                    "name": "userId",
                                    "in": "path",
                                    "required": true,
                                    "type": "integer",
                                    "description": "ID of the user to fetch"
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful response",
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": { "type": "string" },
                                            "email": { "type": "string" }
                                        }
                                    }
                                }
                            }
                        }
                        }
                    }
                    }
              ],
              "communication": "Added POST /users endpoint to support user registration",
            }

            Don't update other parts of the document, only the API contracts.

            If the user message does not require any changes to the API contracts,
            return the same API contracts as the current state.

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        response_format = {
            "updated_doc_element": "updated api contracts",
            "response_message": "communication",
        }
        super().__init__(AgentType.API_CONTRACT, system_message, response_format)

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the chat history and generates a response.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the updated API contracts, communication, and workflow status.
        """
        llm_messages = self.generate_llm_history(chat_history)
        return self.llm.get_response(llm_messages, self.response_format)
