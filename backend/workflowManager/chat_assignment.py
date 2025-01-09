from typing import List, Dict, Any

from agents.types import AgentType
from .models.models import Document, ChatMessage, WorkflowElement


def assign_workflow_element(chat_message):
    document = chat_message.document
    chat_messages = ChatMessage.objects.filter(document=document)
    workflow = document.workflow
    workflow_elements = WorkflowElement.objects.filter(workflow=workflow)
    chat_message.current_workflow_element = _get_workflow_element(
        document, chat_message, chat_messages, workflow_elements
    )
    chat_message.to_agent_type = AgentType[
        chat_message.current_workflow_element.agent.type
    ]
    chat_message.to_id = chat_message.current_workflow_element.agent.type


def _get_workflow_element(document, chat_message, chat_messages, workflow_elements):
    return workflow_elements[0]
