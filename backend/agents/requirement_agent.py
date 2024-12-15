from .agent_interface import AgentInterface
from .llm_wrapper import LLMWrapper
from typing import Any, Tuple
import json

class RequirementAgent(AgentInterface):
    def __init__(self):
        system_message = """
            You are a Requirements Analysis Agent in a system design pipeline. Your role is to:
                1. Analyze and refine incoming requirements
                2. Maintain consistency across all requirements
                3. Identify missing critical requirements
                4. Flag potential conflicts or ambiguities
                5. Ensure requirements are specific, measurable, and achievable

            You will receive a user message and current state of the complete design document in the following JSON format:
            {
                "document": {
                    "requirements": [
                        "Current requirement 1",
                        "Current requirement 2"
                    ],
                    "architecture": {},
                },
                "user_message": "User's input message or requirement"
            }

            For each interaction, you must provide a response in the following JSON format:

            {
                'requirements': [
                    'Detailed requirement description for requirement 1',
                    'Detailed requirement description for requirement 2',
                ],
                'communication': 'Detailed explanation of changes made or reasoning or follow-up questions for clarification',
                'readyForNextWorkflow': boolean
            }

            "example_response_1": {
                "requirements": [
                    "Users must be able to register for an account",
                    "Users must be able to authenticate using email and password",
                ],
                "communication": "Updated authentication requirement to specify password requirements for security compliance",
                "readyForNextWorkflow": false
            }
        """
        
        super().__init__(system_message)
        self.llm = LLMWrapper()

    def process(
        self,
        document: Any,
        user_message: str,
        context: Any = None,
    ) -> Tuple[Any, str, bool]:
        # Generate content string combining document and user message
        content = {
            "document": document,
            "user_message": user_message,
        }
        
        # Convert to JSON string
        content_str = json.dumps(content)

        # Add user message to chat history
        self.chat_history.append({
            "role": "user",
            "content": content_str,
        })
        
        # Get response from LLM
        response = self.llm.get_completion(self.chat_history)
        
        # Add assistant response to chat history
        self.chat_history.append({
            "role": "assistant",
            "content": response,
        })
        
        # Parse the response into a JSON object
        response_json = json.loads(response)

        return response_json["requirements"], response_json["communication"], response_json["readyForNextWorkflow"]
