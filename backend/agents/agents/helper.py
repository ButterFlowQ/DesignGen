from workflowManager.models.models import ChatMessage

def get_message_content(chat: ChatMessage, is_user_agent: bool) -> str:
    """
    Builds the appropriate message content depending on whether the sender is a user or
    an agent.

    :param chat: The ChatMessage being processed.
    :param is_user_agent: True if the sender is the user, False otherwise.
    :param system_type: String describing the type of system (e.g., "architecture")
    :return: A string containing the relevant content for the LLM.
    """
    if is_user_agent:
        if chat.current_document and chat.current_document.workflow_elements:
            text = chat.current_document.workflow_elements
        else:
            text = "{}"
        
        return f"""
            {{
                "document": {text},
                "user_message": {chat.message}
            }}
        """
    else:
        if chat.current_document and chat.current_document.workflow_elements and chat.current_workflow_element and chat.current_workflow_element.json_key in chat.current_document.workflow_elements:
            text = chat.current_document.workflow_elements[chat.current_workflow_element.json_key]
        else:
            text = ""
        
        return f"""
            {{
                {chat.current_workflow_element.json_key}: {text},
                'communication': {chat.message}
            }}
        """
