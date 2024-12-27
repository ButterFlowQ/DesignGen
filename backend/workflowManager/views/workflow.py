import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction

from agents.agent_factory import AgentFactory
from agents.types import AgentType, LLMResponse

from ..models.models import Document, ChatMessage, VersionedDocument, WorkflowElement
from ..chat_assignment import assign_workflow_element

# Create a logger for this module.
logger = logging.getLogger(__name__)

####################################################################################################
########################################## Public Methods ##########################################
####################################################################################################


@csrf_exempt
def send_chat_message(request):
    """
    Public method that receives an incoming chat message from the user,
    validates the request data, creates the new ChatMessage, processes it,
    and returns a JSON-serialized list of messages for the corresponding document.
    """
    logger.info("Received a request to send chat message.")

    if request.method != "POST":
        logger.warning("Invalid request method: %s", request.method)
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        logger.debug("Parsed JSON data: %s", data)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body.")
        return JsonResponse({"error": "Invalid JSON in request body"}, status=400)

    error_response = _validate_chat_message_request(data)
    if error_response:
        logger.warning("Validation failed for request data.")
        return error_response

    chat_message = _build_send_chat_message_response(data, request)
    _process_chat_message(chat_message, request)

    logger.info(
        "Successfully processed chat message with ID: %s for document ID: %s",
        chat_message.id,
        chat_message.document.id if chat_message.document else None,
    )

    return _serialize_chat_messages(_fetch_chat_messages(chat_message.document))


####################################################################################################
########################################## Private Methods #########################################
####################################################################################################


def _validate_chat_message_request(data):
    """
    Private method that validates the basic fields required for a chat message request.
    Returns a JsonResponse if any required field is missing or invalid; otherwise None.
    """
    logger.debug("Validating chat message request data.")
    required_fields = ["message", "document_id", "in_reply_to"]
    for field in required_fields:
        if field not in data:
            logger.warning("Missing required field: %s", field)
            return JsonResponse(
                {"error": f"Missing required field: {field}"}, status=400
            )
    return None


####################################################################################################


def _build_send_chat_message_response(data, request):
    """
    Private method that extracts data from the request and creates a ChatMessage object.
    """
    logger.debug("Building chat message from request data.")
    document = get_object_or_404(Document, pk=data["document_id"])
    in_reply_to = get_object_or_404(ChatMessage, pk=data["in_reply_to"])

    chat_message = ChatMessage.objects.create(
        message=data["message"],
        document=document,
        in_reply_to=in_reply_to,
        from_agent_type=AgentType.USER,
        from_id=request.user.id,  # Ensure user is authenticated
    )

    logger.info(
        "Created a new ChatMessage (ID: %s) for Document ID: %s",
        chat_message.id,
        document.id,
    )
    return chat_message


####################################################################################################


def _fetch_chat_messages(document):
    """
    Private method that returns all ChatMessage objects for a given Document.
    """
    logger.debug("Fetching chat messages for Document ID: %s", document.id)
    return ChatMessage.objects.filter(document=document)


####################################################################################################


def _serialize_chat_messages(chat_messages):
    """
    Private method that serializes a list of ChatMessage objects into JSON response.
    """
    logger.debug("Serializing %d chat messages.", len(chat_messages))
    response_data = [
        {
            "id": msg.id,
            "message": msg.message,
            "from_agent_type": msg.from_agent_type,
            "from_id": msg.from_id,
            "to_agent_type": msg.to_agent_type,
            "to_id": msg.to_id,
            "current_document": (
                msg.current_document.id if msg.current_document else None
            ),
        }
        for msg in chat_messages
    ]
    return JsonResponse(response_data, safe=False)


####################################################################################################


def _process_chat_message(chat_message, request):
    """
    Private method that coordinates:
      1) Assigning the appropriate workflow element to the chat message
      2) Generating a response from the LLM agent
      3) Handling the resulting LLM response (possibly recursively)
    """
    logger.info(
        "Processing ChatMessage ID: %s for Document ID: %s",
        chat_message.id,
        chat_message.document.id if chat_message.document else None,
    )

    assign_workflow_element(chat_message)
    chat_message.save()

    document = chat_message.document
    chat_messages = _fetch_chat_messages(document)

    llm_response = AgentFactory.create_agent(
        AgentType[chat_message.current_workflow_element.agent.id]
    ).process(chat_messages)

    logger.debug(
        "LLM response for ChatMessage ID %s: %s", chat_message.id, llm_response
    )

    new_chat_message = _handle_llm_response(
        llm_response, document, chat_message.current_workflow_element, request
    )

    if llm_response["move_to_next_workflow"]:
        logger.info("LLM indicates move to next workflow. Processing next step.")
        _process_chat_message(new_chat_message, request)


####################################################################################################


@transaction.atomic
def _handle_llm_response(
    llm_response: LLMResponse,
    document: Document,
    workflow_element: WorkflowElement,
    request,
):
    """
    Private method that applies the LLM response to update document versions,
    creates a new ChatMessage from the agent, and returns the newly-created chat message.
    """
    logger.debug(
        "Handling LLM response for Document ID: %s, WorkflowElement ID: %s",
        document.id,
        workflow_element.id,
    )

    updated_content = llm_response["updated_workflow_doc"]
    logger.info(
        "Updating document version from %d to %d",
        document.latest_version,
        document.latest_version + 1,
    )
    document.latest_version += 1

    previous_version = VersionedDocument.objects.filter(document=document).latest(
        "version"
    )
    logger.debug(
        "Previous VersionedDocument ID: %s (version %d)",
        previous_version.id,
        previous_version.version,
    )

    # Create a new VersionedDocument record from the old one
    new_version = VersionedDocument.objects.create(
        document=document,
        version=document.latest_version,
        workflow_elements=previous_version.workflow_elements or {},
    )

    logger.debug(
        "New VersionedDocument ID: %s created with version %d",
        new_version.id,
        new_version.version,
    )

    # Update the relevant workflow element's content
    new_version.workflow_elements[workflow_element.id] = updated_content
    new_version.save()
    document.save()

    # Create a new ChatMessage from the agent
    chat_message = ChatMessage.objects.create(
        document=document,
        message=llm_response["response_message"],
        from_agent_type=AgentType[workflow_element.agent.id],
        from_id=workflow_element.agent.id,
        to_id=request.user.id,
        to_agent_type=AgentType.USER,
        current_document=new_version,
    )

    logger.info(
        "Created a new ChatMessage from agent (ID: %s) with content: '%s'",
        chat_message.id,
        llm_response["response_message"],
    )

    # Move to next workflow if required
    if llm_response["move_to_next_workflow"]:
        logger.info("Moving Document ID %s to next workflow.", document.id)
        document.workflow = document.workflow.next_workflow
        document.save()

    return chat_message
