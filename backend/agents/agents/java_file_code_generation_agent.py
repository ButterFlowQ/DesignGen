from typing import List

from agents.types import AgentType, LLMResponse
from orchestrator.models.models import ChatMessage

from .simple_agent_interface import SimpleAgentInterface


class JavaFileCodeGenerationAgent(SimpleAgentInterface):
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
                },
                "file name": "Name of the file to be generated",
            }

            For each interaction, you must provide a response in the following JSON format:
            {
                "file content": "Complete file content as string",
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
            "updated_doc_element": "file content",
            "response_message": "communication",
        }
        super().__init__(
            AgentType.JAVA_FILE_CODE_GENERATOR,
            system_message,
            response_format,
        )

    def process(self, message: str) -> LLMResponse:
        llm_messages = self.generate_llm_history(message)
        return self.llm.get_response(llm_messages, self.response_format)