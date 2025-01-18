from workflowManager.models.models import ChatMessage

def get_message_content(chat: ChatMessage, is_user_agent: bool, system_type: str) -> str:
    """
    Builds the appropriate message content depending on whether the sender is a user or
    an agent.

    :param chat: The ChatMessage being processed.
    :param is_user_agent: True if the sender is the user, False otherwise.
    :param system_type: String describing the type of system (e.g., "architecture")
    :return: A string containing the relevant content for the LLM.
    """
    if is_user_agent:
        # Retrieve the relevant document (if it exists)
        if chat.document:
            document_text = get_relevant_document(chat.document)
        else:
            document_text = "No document available."

        return (
            f"{chat.message}\n\n"
            f"Based on the document provided below, please propose or update the {system_type}:\n"
            f"Document:\n{document_text}"
        )
    return chat.message

def get_relevant_document(document) -> str:
    """
    Returns a string representation of the given document. If you need more complex
    behavior (e.g., extracting only specific fields), adapt this method accordingly.

    :param document: The Document object or a related entity from ChatMessage.
    :return: A string representing the document content.
    """
    return str(document)
