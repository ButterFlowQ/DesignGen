import json
import logging

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from ..models.models import Document, Workflow, VersionedDocument

logger = logging.getLogger(__name__)


####################################################################################################
########################################## Public Methods ##########################################
####################################################################################################


@csrf_exempt
@login_required
def create_document(request):
    """
    Creates a new Document and its initial VersionedDocument.
    Expects a POST request with JSON containing:
      {
        "workflow": <workflow_id> (required),
        "latest_version": <int>,
        "title": <str> (required)
      }
    Returns JSON with:
      {
        "id": <new_document_id>,
        "versioned_document_id": <new_versioned_document_id>
      }
    """
    logger.info("Received request to create a document.")

    if request.method != "POST":
        logger.warning("Invalid request method: %s (expected POST).", request.method)
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        logger.debug("Parsed JSON data for create_document: %s", data)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body for create_document.")
        return JsonResponse({"error": "Invalid JSON in request body"}, status=400)

    validation_error_response = _validate_create_document_request_data(data)
    if validation_error_response:
        return validation_error_response

    try:
        with transaction.atomic():
            document = _create_document_from_data(request, data)
            versioned_document = _create_versioned_document_from_data(document, data)
    except ValidationError as ve:
        logger.warning("ValidationError while creating document: %s", ve)
        return JsonResponse({"error": str(ve)}, status=400)
    except Exception as e:
        logger.error("Error while creating Document or VersionedDocument: %s", e)
        return JsonResponse({"error": "Failed to create document"}, status=500)

    logger.info(
        "Created Document (ID=%s) with VersionedDocument (ID=%s).",
        document.id,
        versioned_document.id,
    )

    return JsonResponse(
        {"id": document.id, "versioned_document_id": versioned_document.id}, status=201
    )


####################################################################################################


@csrf_exempt
@login_required
def get_document(request, document_id):
    """
    Retrieves a Document by its ID, returning its latest version info.
    Expects a GET request.

    Checks if the logged-in user can access the requested document.
    Returns JSON with:
      {
        "id": <document_id>,
        "workflow": <workflow_id>,
        "owner": <owner_id>,
        "latest_version": <document_latest_version>,
        "title": <latest_versioned_document_title>,
        "version": <latest_versioned_document_version>,
        "workflow_elements": <latest_versioned_document_elements>,
      }
    """
    logger.info("Received request to get Document with ID: %s", document_id)

    if request.method != "GET":
        logger.warning("Invalid request method: %s (expected GET).", request.method)
        return JsonResponse({"error": "Invalid request method"}, status=400)
    error, document = _validate_get_document_request_data(document_id, request.user)
    if error:
        return error

    logger.debug(
        "Found Document (ID=%s). Latest version is %s.",
        document.id,
        document.latest_version,
    )

    try:
        versioned_document = VersionedDocument.objects.filter(document=document).latest(
            "version"
        )
        logger.debug(
            "Fetched latest VersionedDocument (ID=%s, version=%s).",
            versioned_document.id,
            versioned_document.version,
        )
    except VersionedDocument.DoesNotExist:
        logger.warning(
            "No VersionedDocument found for Document (ID=%s).",
            document.id,
        )
        return JsonResponse({"error": "No versioned document found"}, status=404)

    response = {
        "id": document.id,
        "workflow": document.workflow.id if document.workflow else None,
        "owner": document.owner.id if document.owner else None,
        "latest_version": document.latest_version,
        "title": versioned_document.title,
        "version": versioned_document.version,
        "workflow_elements": versioned_document.workflow_elements,
    }

    logger.info("Successfully retrieved Document (ID=%s).", document.id)
    return JsonResponse(response, status=200)


####################################################################################################
########################################## Private Methods #########################################
####################################################################################################


def _validate_create_document_request_data(data):
    """
    Checks whether the required fields ('workflow' and 'title') are present
    in the data and returns a JsonResponse if there's a problem. Otherwise None.
    """
    logger.debug("Validating create_document request data.")
    missing_fields = []
    for field in ["workflow", "title"]:
        if field not in data:
            missing_fields.append(field)

    if missing_fields:
        logger.warning(
            "Missing required fields for create_document: %s", missing_fields
        )
        return JsonResponse(
            {"error": f"Missing required fields: {', '.join(missing_fields)}"},
            status=400,
        )

    return None


####################################################################################################


def _validate_get_document_request_data(document_id: int, user):
    """
    Private helper method that:
      1. Retrieves the Document by its ID.
      2. Checks if it exists (returns a 404 JsonResponse if not).
      3. Checks if the user has permission to access it (returns 403 if not).
      4. Returns the Document object if everything is valid.

    Otherwise, returns a JsonResponse indicating the error.
    """
    # Retrieve the document
    document = Document.objects.filter(id=document_id).first()
    if not document:
        logger.warning("Document not found for ID: %s", document_id)
        return JsonResponse({"error": "Document not found"}, status=404)

    # Check permissions
    if not _user_can_access_document(user, document):
        logger.warning(
            "User %s attempted to access Document ID %s without permission.",
            user.username,
            document.id,
        )
        return JsonResponse({"error": "Permission denied"}, status=403), None

    # If everything is fine, return the Document
    return None, document


####################################################################################################


def _create_document_from_data(request, data):
    """
    Private helper function that creates and returns a new Document
    based on the validated JSON data and the authenticated user.
    Raises ValidationError if the workflow is not found.
    """
    workflow_id = data["workflow"]
    latest_version = data.get("latest_version", 0)

    logger.debug(
        "Creating Document with workflow_id=%s, latest_version=%s",
        workflow_id,
        latest_version,
    )

    workflow = Workflow.objects.filter(id=workflow_id).first()
    if not workflow:
        logger.warning("Workflow ID %s not found. Cannot create Document.", workflow_id)
        raise ValidationError(f"Workflow with ID {workflow_id} does not exist.")

    document = Document.objects.create(
        workflow=workflow,
        owner=request.user,
        latest_version=latest_version,
    )

    logger.info(
        "Document created (ID=%s) for user: %s",
        document.id,
        request.user.username if request.user.is_authenticated else "Anonymous",
    )

    return document


####################################################################################################


def _create_versioned_document_from_data(document, data):
    """
    Private helper function that creates and returns a new VersionedDocument,
    using the provided Document and data for the title/initial version.
    """
    title = data["title"]
    logger.debug(
        "Creating VersionedDocument for Document (ID=%s) with title='%s'",
        document.id,
        title,
    )

    versioned_document = VersionedDocument.objects.create(
        document=document, title=title, version=0  # default initial version
    )

    logger.info(
        "VersionedDocument created (ID=%s) for Document (ID=%s).",
        versioned_document.id,
        document.id,
    )

    return versioned_document


####################################################################################################


def _user_can_access_document(user, document):
    """
    Private helper function that returns True if the given user can access
    the specified document. Otherwise returns False.

    This simplest check ensures the user is the document's owner.
    For more complex logic, expand this function (e.g., user roles,
    shared permissions, group membership, etc.).
    """
    if not user.is_authenticated:
        return False
    return document.owner == user
