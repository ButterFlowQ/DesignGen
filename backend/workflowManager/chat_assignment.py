from typing import Any, Dict, List

from agents.llm_wrapper import LLMWrapper
from agents.types import AgentType, LLMMessage, LLMResponse

from .models.models import ChatMessage, Document, WorkflowElement


class ChatAssignment:
    def __init__(self):
        self.llm = LLMWrapper()

    def assign_workflow_element(self, chat_message):
        document = chat_message.document
        chat_messages = ChatMessage.objects.filter(document=document)
        workflow = document.workflow
        workflow_elements = WorkflowElement.objects.filter(workflow=workflow)
        chat_message.current_workflow_element = self._get_workflow_element(
            document, chat_message, chat_messages, workflow_elements
        )
        chat_message.to_agent_type = AgentType[
            chat_message.current_workflow_element.agent.type
        ]
        chat_message.to_id = chat_message.current_workflow_element.agent.type

    def _get_workflow_element(
        self, document, chat_message, chat_messages, workflow_elements
    ):
        if not chat_messages:
            return workflow_elements[0]
        llm_messages: List[LLMMessage] = []
        workflow_element_prompts = {}
        for workflow_element in workflow_elements:
            workflow_element_prompts[workflow_element.id] = [
                workflow_element.relevancy_checking_prompt
            ]

        system_message = self._build_system_prompt(workflow_element_prompts)

        # Add the system message as the first message
        llm_messages.append({"role": "system", "content": system_message})
        for chat in chat_messages:
            # Compare the enum's value to the stored string
            is_requirement_agent = chat.from_agent_type == AgentType.REQUIREMENT.value
            is_user_agent = chat.from_agent_type == AgentType.USER.value

            role = "assistant" if is_requirement_agent else "user"
            message_content = self._get_message_content(chat, is_user_agent)
            llm_messages.append({"role": role, "content": message_content})
        response_format = {"agent_id": "agent_id"}
        llm_response = self.llm.get_response(llm_messages, response_format)
        assigned_element = int(llm_response["agent_id"])
        for workflow_element in workflow_elements:
            if workflow_element.id == assigned_element:
                return workflow_element
        raise ValueError("No workflow element found")

    def _build_system_prompt(self, workflow_element_prompts):
        """
        Combines all agent descriptions into a single system prompt that instructs the model
        to determine which agent is responsible for the last message.
        """
        instructions = (
            "You are an AI that determines which agent should handle the last user message.\n\n"
            "We have multiple agents with different responsibilities, it is of format **<agent_id>**: <responsiblity>:\n"
        )

        for agent_name, prompt_text in workflow_element_prompts.items():
            instructions += f"**{agent_name}**: {prompt_text}\n"

        instructions += (
            "\nPlease read the conversation and decide which agent name is the best match for the last message. "
            "Your answer should be exactly one of the agent names defined above."
            "For each interaction, you must provide a response in the following JSON format:\n\n"
            "{\n"
            "  'agent_id': 'agent_id'\n"
            "}\n\n"
        )

        return instructions

    def _get_message_content(self, chat: ChatMessage, is_user_agent: bool) -> str:
        """
        Builds the appropriate message content depending on whether the sender is a user or
        the Agent.

        :param chat: The ChatMessage being processed.
        :param is_user_agent: True if the sender is the user, False otherwise.
        :return: A string containing the relevant content for the LLM.
        """
        if is_user_agent:
            # Retrieve the relevant document (if it exists)
            if chat.document:
                document_text = chat.document.text
            else:
                document_text = "No document available."

            return (
                f"{chat.message}\n\n"
                "Update the doc given below as desired:\n"
                f"Document:\n{document_text}"
            )
        return chat.message
