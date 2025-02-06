import json
from typing import List

from agents.types import AgentType, LLMResponse
from orchestratorV2.models import ChatMessage

from .agent_interface import AgentInterface
from .java_lld_html_generator_agent import JavaLLDHTMLGeneratorAgent


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
                2. Design classes across controllers, dtos, services, repositories, and entities layers
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
                    "java LLD": [...],
                },
                "user_message": "User's input or request regarding class design"
            }

            For each interaction, you must provide a response in the following JSON format:

            {
                "updated java LLD": {
                    "controllers": [
                        {controller classes or interfaces},
                        {... other controller classes or interfaces},
                    ],
                    "dtos": [
                        {
                            "type": "dto class",
                            "name": "ClassName",
                            "description": "Description of the dto class",
                            "package": "com.example.projectname.dtos",
                            "fields": [
                                {
                                    "name": "fieldName",
                                    "type": "fieldType",
                                    "has_getter": true/false,
                                    "has_setter": true/false,
                                },
                                {... other fields},
                            ],
                        },
                        {... other dtos},
                    ],
                    "services": [
                        {
                            "type": "class",
                            "name": "ClassName",
                            "description": "Description of the service class",
                            "package": "com.example.projectname.services",
                            "extends": [optional_parent_class, ...],
                            "implements": [optional_parent_interface, ..., ...],
                            "dependencies": [
                                {
                                    "name": "dependencyName",
                                    "type": "dependencyType",
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
                    "repositories": [
                        {
                            "type": "interface",
                            "name": "InterfaceName",
                            "package": "com.example.projectname.repositories",
                            "description": "Description of the repository interface",
                            "extends": [optional_parent_interface, ...],
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
                            ]
                        },
                        {... other classes or interfaces},
                    ],
                    "entities": [
                        {
                            "type": "entity class",
                            "name": "ClassName",
                            "description": "Description of the entity class",
                            "package": "com.example.projectname.entities",
                            "fields": [
                                {
                                    "name": "fieldName",
                                    "type": "fieldType",
                                    "has_getter": true/false,
                                    "has_setter": true/false,
                                },
                                {... other fields},
                            ],
                        },
                        {... other entities},
                    ],
                    "enums": [
                    {
                        "type": "enum class",
                        "name": "EnumName",
                        "description": "Description of the enum class",
                        "package": "com.example.projectname.enums",
                        "fields": [
                            {
                                "name": "fieldName",
                                "type": "fieldType",
                            },
                            {... other fields},
                        ],
                    },
                    {... other enums},
                    ],
                    "configurations": [
                        {   
                            "type": "class",
                            "name": "ClassName",
                            "description": "Description of the configuration class",
                            "package": "com.example.projectname.configurations",
                            "extends": [optional_parent_interface, ...],
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
                                    ],
                                },
                                {...},
                            ],
                            "fields": [
                                {
                                    "name": "fieldName",
                                    "type": "fieldType",
                                    "has_getter": true/false,
                                    "has_setter": true/false,
                                },
                                {... other fields},
                            ],
                        },
                        {... other configurations},
                    ],
                },
                "communication": "Explanation of the class design decisions and patterns used",
            }

            Follow these guidelines:
            1. Repository classes should handle database operations
            2. Service classes should contain business logic
            3. Controller classes should handle HTTP requests
            4. DTO classes should handle data transfer between layers
            5. Entities classes should handle database entities
            6. Follow Java naming conventions
            7. Use appropriate design patterns where applicable

            Don't update other parts of the document, only the class designs.

            If the user message does not require any changes to the class designs,
            return the same class designs as the current state.

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_doc_element": "updated java LLD",
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
        llm_messages = self.generate_llm_history(chat_history, AgentType.JAVA_LLD)
        llm_response = self.llm.get_response(llm_messages, self.response_format)

        java_lld_html_generator = JavaLLDHTMLGeneratorAgent()

        uml = java_lld_html_generator.process(
            json.dumps(llm_response["updated_doc_element"])
        )["response_message"]
        llm_response["updated_doc_element"] = uml
        return llm_response
