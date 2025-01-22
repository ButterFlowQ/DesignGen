from workflowManager.models.models import ChatMessage

def get_message_content(chat: ChatMessage) -> str:
    """
    Builds the appropriate message content depending on whether the sender is a user or
    an agent.

    :param chat: The ChatMessage being processed.
    :return: A string containing the relevant content for the LLM.
    """
    if chat.is_user_message:
        return (
            f"User message: {chat.message}\n\n"
            f"Please update the {chat.name} in the document provided below, as per the user message:\n"
            f"{chat.current_document.document_elements}"
        )
    
    else:
        return chat.llm_raw_response
