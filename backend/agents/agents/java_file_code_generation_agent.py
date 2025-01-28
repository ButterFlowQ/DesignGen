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
            1. Generate actual java code implementation based on the complete system design document for the given file
            2. Follow best practices and coding standards
            3. Implement the designed class or interface, and methods
            4. Include all necessary imports
            5. Include appropriate comments and documentation
            6. Create extra methods if necessary to keep the code clean and modular

            You will receive a user message and the current state of the complete design document in the following JSON format.
            Focus mainly on java LLD to generate the java file code.
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