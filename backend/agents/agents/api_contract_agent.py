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
                            },
                            ... other methods
                        },
                        ... other paths
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
        llm_messages = self.generate_llm_history(chat_history, AgentType.API_CONTRACT)
        response = self.llm.get_response(llm_messages, self.response_format)
        response["html_response"] = self.get_html(response["updated_doc_element"])
        return response

    def get_html(self, api_contracts: List[dict]) -> str:
        """
        Converts API contracts into HTML format using tables.
        
        :param api_contracts: List of API contract dictionaries in Swagger format
        :return: HTML formatted string containing the API contracts
        """
        if not api_contracts:
            return "<p>No API contracts defined yet.</p>"
            
        html = "<div class='api-contracts'>\n"
        html += "<style>\n"
        html += ".api-table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }\n"
        html += ".api-table th, .api-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n"
        html += ".api-table th { background-color: #f5f5f5; }\n"
        html += ".api-table ul { margin: 0; padding-left: 20px; }\n"
        html += "</style>\n"
        
        html += "<h3>API Contracts:</h3>\n"
        
        for contract in api_contracts:
            info = contract.get("info", {})
            paths = contract.get("paths", {})
            
            html += f"<h4>{info.get('title', 'Untitled API')} (v{info.get('version', 'n/a')})</h4>\n"
            html += "<table class='api-table'>\n"
            html += "<thead>\n"
            html += "    <tr>\n"
            html += "        <th>Method</th>\n"
            html += "        <th>Path</th>\n"
            html += "        <th>Summary</th>\n"
            html += "        <th>Parameters</th>\n"
            html += "        <th>Responses</th>\n"
            html += "    </tr>\n"
            html += "</thead>\n"
            html += "<tbody>\n"
            
            for path, methods in paths.items():
                for method, details in methods.items():
                    html += "    <tr>\n"
                    html += f"        <td><strong>{method.upper()}</strong></td>\n"
                    html += f"        <td>{path}</td>\n"
                    html += f"        <td>{details.get('summary', 'No summary')}</td>\n"
                    
                    # Parameters column
                    params = details.get("parameters", [])
                    html += "        <td>\n"
                    if params:
                        html += "            <ul>\n"
                        for param in params:
                            html += f"                <li>{param.get('name')} ({param.get('in')})"
                            if param.get('description'):
                                html += f": {param.get('description')}"
                            html += "</li>\n"
                        html += "            </ul>\n"
                    else:
                        html += "            None"
                    html += "        </td>\n"
                    
                    # Responses column
                    responses = details.get("responses", {})
                    html += "        <td>\n"
                    if responses:
                        html += "            <ul>\n"
                        for status, response in responses.items():
                            html += f"                <li>{status}: {response.get('description', 'No description')}</li>\n"
                        html += "            </ul>\n"
                    else:
                        html += "            None"
                    html += "        </td>\n"
                    html += "    </tr>\n"
            
            html += "</tbody>\n"
            html += "</table>\n"
        
        html += "</div>"
        return html
