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
    # Retrieve the relevant document (if it exists)
    if chat.current_document and chat.current_document.workflow_elements and chat.current_workflow_element and chat.current_workflow_element.position in chat.current_document.workflow_elements:
            document_text = chat.current_document.workflow_elements[chat.current_workflow_element.position]
    else:
        document_text = "No document available."

    if is_user_agent:

        agent_type = chat.to_agent_type
        return (
            f"{chat.message}\n\n"
            f"Based on the document provided below, please propose or update the {agent_type}:\n"
            f"Document:\n{document_text}"
        )
    
    agent_type = chat.from_agent_type
    # document_text = chat.current_document.workflow_elements[chat.current_workflow_element.id]
    return (
        f"{chat.message}\n\n"
        f"Updated {agent_type}:\n{document_text}"
    )
