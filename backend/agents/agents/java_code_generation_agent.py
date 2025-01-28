from typing import List

from agents.types import AgentType, LLMResponse
from orchestrator.models.models import ChatMessage

from .agent_interface import AgentInterface


class JavaCodeGenerationAgent(AgentInterface):
    """
    An agent responsible for generating java code based on the system design document.
    Takes the complete design document as input and generates actual java code files.
    """

    def __init__(self) -> None:
        """
        Initializes the CodeGenerationAgent with a system message and response format.
        """
        system_message = """
            You are a Java Code Generation Agent in a system design pipeline. Your role is to:
            1. Generate actual java code implementation based on the complete system design document
            2. Follow best practices and coding standards
            3. Implement the designed classes, interfaces, and methods
            4. Generate code that matches the specified architecture and design patterns

            You will receive a user message and the current state of the complete design document in the following JSON format.
            Focus mainly on java LLD to generate the java code.
            {
                "document": {
                    "functional requirements": [...],
                    "non functional requirements": [...],
                    "architecture": {...},
                    "api contracts": [...],
                    "database schema": [...],
                    "java LLD": [...],
                    "java code": [...],
                },
                "user_message": "User's input or request regarding code generation"
            }

            For each interaction, you must provide a response in the following JSON format:
            {
                "updated java code": [
                    {
                        "path": "com/example/projectname/controllers/ClassName.java",
                        "content": "Complete file content as string"
                    },
                    {
                        "path": "com/example/projectname/services/ClassName.java",
                        "content": "Complete file content as string"
                    },
                    {...},
                ],
                "communication": "Explanation of the generated code and implementation decisions"
            }

            Follow these guidelines:
            1. Generate complete, working code files
            2. Include all necessary imports
            3. Follow the package structure defined in the java LLD
            4. Implement all methods specified in the interfaces
            5. Follow coding standards and best practices
            6. Include appropriate comments and documentation

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_doc_element": "updated java code",
            "response_message": "communication",
        }
        super().__init__(
            AgentType.JAVA_CODE_GENERATOR,
            system_message,
            response_format,
            "openai:gpt-4o-2024-08-06",
        )

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the given chat history by generating LLM messages and querying the LLM for a
        structured response containing generated code files.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the generated code files, communication, dependencies,
                and a boolean indicating whether to move to the next workflow.
        """
        llm_messages = self.generate_llm_history(chat_history, agent_type=AgentType.JAVA_CODE_GENERATOR)
        return self.llm.get_response(llm_messages, self.response_format)
