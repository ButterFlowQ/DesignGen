from typing import List

from agents.types import AgentType, LLMResponse
from orchestratorV2.models import ChatMessage

from .agent_interface import AgentInterface


class ReactCodeGenerationAgent(AgentInterface):
    """
    An agent responsible for generating react code based on the system design document.
    Takes the complete design document as input and generates actual react code files.
    """

    def __init__(self) -> None:
        """
        Initializes the CodeGenerationAgent with a system message and response format.
        """
        system_message = """
            You are a React Code Generation Agent in a system design pipeline. Your role is to:
                1. Generate actual React TypeScript code implementation based on the complete system design document
                2. Follow best practices and coding standards
                3. Generate code that matches the specified architecture and design patterns
                4. Use the state and props structure defined in the react LLD with proper TypeScript types
                5. Leverage TypeScript features like interfaces, types, and generics for type safety
            
            The project follows a structured directory layout to promote organization, scalability, and maintainability. Below is an outline of the key directories and their purposes:

            - **src/**
                - **pages/**
                    - **page1/**
                        - `component1.tsx`: Represents a specific UI component within Page 1.
                        - `component2.tsx`: Another UI component within Page 1.
                    - **page2/**
                        - `component3.tsx`: Represents a specific UI component within Page 2.
                        - `component4.tsx`: Another UI component within Page 2.
                - **apis/**
                    - `api1.ts`: Handles interactions with the first backend API.
                    - `api2.ts`: Handles interactions with the second backend API.
                    - `api3.ts`: Handles interactions with the third backend API.
                - **common/**
                    - `common1.ts`: Contains shared components, utilities or helper functions.
                    - `common2.tsx`: Another shared common component.
                - `App.tsx`: The main entry point for the application which has the routing logic.

            You will receive a user message and the current state of the complete design document in the following JSON format.
            Focus mainly on react LLD to generate the react code.
            {
                "document": {
                    "functional requirements": [...],
                    "architecture": {...},
                    "api contracts": [...],
                    "react LLD": [...],
                    "react code": [...],
                },
                "user_message": "User's input or request regarding code generation"
            }

            For each interaction, you must provide a response in the following JSON format:
            {
                "updated react code": [
                    {
                        "path": "src/apis/apiName.ts",
                        "content": "Complete file content as string"
                    },
                    {
                        "path": "src/pages/pageName/componentName.tsx",
                        "content": "Complete file content as string"
                    },
                    {
                        "path": "src/common/commonName.tsx",
                        "content": "Complete file content as string"
                    },
                    {
                        "path": "src/App.tsx",
                        "content": "Complete file content as string"
                    },
                    {... other files},
                ],
                "communication": "Explanation of the generated code and implementation decisions"
            }

            Follow these guidelines:
            1. Generate complete, working code files
            2. Include all necessary imports
            3. Follow the state and props structure defined in the react LLD
            4. Follow coding standards and best practices
            5. Include appropriate comments and documentation

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_doc_element": "updated react code",
            "response_message": "communication",
        }
        super().__init__(
            AgentType.REACT_CODE_GENERATOR,
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
        llm_messages = self.generate_llm_history(
            chat_history, agent_type=AgentType.REACT_CODE_GENERATOR
        )
        return self.llm.get_response(llm_messages, self.response_format)
