from typing import List

from agents.types import AgentType, LLMResponse
from orchestrator.models.models import ChatMessage

from .agent_interface import AgentInterface


class JavaLLDAgent(AgentInterface):
    """
    An agent responsible for creating low-level design details for Java applications,
    including interfaces, class structures, and their relationships across repository,
    service, and controller layers.
    """

    def __init__(self) -> None:
        """
        Initializes the JavaLLDAgent with a system message and a specified response format.
        """
        system_message = """
            You are a Java Low Level Design Agent in a system design pipeline. Your role is to:
                1. Create detailed low level design including interfaces, classes (leave out method implementations in classes), enums.
                2. Design classes across repository, service, and controller layers
                3. Follow SOLID principles and design patterns
                4. Ensure proper separation of concerns

            You will receive a user message and the current state of the complete design document in the following JSON format.
            Focus mainly on database schema and api contracts to update the class designs.

            {
                "document": {
                    "functional requirements": [...],
                    "non functional requirements": [...],
                    "architecture": {...},
                    "api contracts": [...],
                    "database schema": [...],
                    "low level design": [...],
                },
                "user_message": "User's input or request regarding class design"
            }

            For each interaction, you must provide a response in the following JSON format:

            {
                "updated low level design": {
                    "repositories": [
                        {
                            "type": "interface",
                            "name": "interfaceName",
                            "package": "com.example.projectname.repository",
                            "extends": "optional_parent_interface",
                            "methods": [
                                {
                                    "name": "methodName",
                                    "return_type": "returnType",
                                    "parameters": [
                                        {
                                            "name": "paramName",
                                            "type": "paramType"
                                        },
                                        {...},
                                    ]
                                }
                                {...},
                                {...},
                            ]
                        },
                        {... other classes or interfaces},
                    ],
                    "services": [
                        {
                            "type": "class",
                            "name": "className",
                            "package": "com.example.projectname.service",
                            "extends": [optional_parent_class, ...],
                            "implements": [optional_parent_interface, ..., ...],
                            "fields": [
                                {
                                    "name": "fieldName",
                                    "type": "fieldType",
                                    "visibility": "private/public/protected"
                                },
                                {...},
                                {...},
                            ],
                            "methods": [
                                {
                                    "name": "methodName",
                                    "visibility": "public/private/protected",
                                    "return_type": "returnType",
                                    "parameters": [
                                        {
                                            "name": "paramName",
                                            "type": "paramType"
                                        },
                                        {...},
                                    ]
                                },
                                {...},
                            ]
                        },
                        {... other classes or interfaces},
                    ],
                    "controllers": [
                        {...},
                        {...},
                        {...},
                    ]
                },
                "communication": "Explanation of the class design decisions and patterns used",
            }

            Follow these guidelines:
            1. Repository classes should handle database operations
            2. Service classes should contain business logic
            3. Controller classes should handle HTTP requests
            4. Follow Java naming conventions
            5. Use appropriate design patterns where applicable

            Don't update other parts of the document, only the class designs.

            If the user message does not require any changes to the class designs,
            return the same class designs as the current state.

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_doc_element": "updated low level design",
            "response_message": "communication",
        }
        super().__init__(AgentType.JAVA_LLD, system_message, response_format)

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the given chat history by generating LLM messages and querying the LLM for a
        structured response containing detailed Java class designs.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the class designs, communication, dependencies,
                and a boolean indicating whether to move to the next workflow.
        """
        llm_messages = self.generate_llm_history(chat_history)
        return self.llm.get_response(llm_messages, self.response_format)
