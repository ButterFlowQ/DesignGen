from typing import List

from workflowManager.models import ChatMessage

from .agent_interface import AgentInterface
from .types import AgentType, LLMMessage, LLMResponse


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
                'ready_for_next_workflow': boolean
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

        response_format = ["requirements", "communication", "ready_for_next_workflow"]
        super().__init__(AgentType.REQUIREMENT, system_message, response_format)

    def process(
        self,
        chat_history: List[ChatMessage],
    ) -> LLMResponse:

        llm_messages = self.generate_llm_history(chat_history)

        # Get response from LLM
        return self.llm.get_response(llm_messages, self.response_format)

    def generate_llm_history(self, chat_history: List[ChatMessage]) -> List[LLMMessage]:

        llm_messages: List[LLMMessage] = []

        # Add system message
        llm_messages.append(self.system_message)

        # Convert chat history to LLM messages
        for chat in chat_history:
            is_requirement_agent = chat.from_agent_type == str(AgentType.REQUIREMENT)
            is_user_agent = chat.from_agent_type == str(AgentType.USER.value)

            message: LLMMessage = {
                "role": "assistant" if is_requirement_agent else "user",
                "content": self.get_message_content(chat, is_user_agent),
            }
            llm_messages.append(message)

        return llm_messages

    def get_message_content(self, chat: ChatMessage, is_user_agent: bool) -> str:
        if is_user_agent:
            return f"""{chat.message}
                        Update the requirements in the doc given below as desired:
                        Document:
                        {self.get_relevant_document(chat['document'])}
                    """
        else:
            return chat.message

    def get_relevant_document(self, document: str) -> str:
        return document
