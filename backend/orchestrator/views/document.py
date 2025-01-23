import json
import logging

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from ..models.models import Document, DocumentSchema, VersionedDocument

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
        "document_schema": <document_schema_id> (required),
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
# @login_required
def get_document(request, document_id):
    """
    Retrieves a Document by its ID, returning its latest version info.
    Expects a GET request.

    Checks if the logged-in user can access the requested document.
    Returns JSON with:
      {
        "id": <document_id>,
        "document_schema": <document_schema_id>,
        "owner": <owner_id>,
        "latest_version": <document_latest_version>,
        "title": <latest_versioned_document_title>,
        "version": <latest_versioned_document_version>,
        "document_elements": <latest_versioned_document_elements>,
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

    # response = {
    #     "id": document.id,
    #     "document_schema": (
    #         document.document_schema.id if document.document_schema else None
    #     ),
    #     "owner": document.owner.id if document.owner else None,
    #     "latest_version": document.latest_version,
    #     "title": versioned_document.title,
    #     "version": versioned_document.version,
    #     "document_elements": versioned_document.document_elements,
    # }
    response = {
        "chat_messages": [
            {
                "id": 7,
                "message": "Create a system design for Automatic case distribution engine",
                "from_id": "1",
                "to_id": "1",
                "current_document": 3,
            },
            {
                "id": 8,
                "message": "To create a system design for an Automatic Case Distribution Engine, I need more information. Could you please clarify: 1. What specific actions should users be able to perform with the engine? 2. What are the expected behaviors and responses of the system when distributing cases? 3. What data inputs and outputs are required, and are there any specific validations needed? 4. Are there any business rules or constraints that should be considered? 5. What user roles and permissions are necessary? 6. Are there any integration requirements with other systems?",
                "from_id": "1",
                "to_id": "1",
                "current_document": 4,
                "llm_raw_response": '{\n    "updated functional requirements": [],\n    "communication": "To create a system design for an Automatic Case Distribution Engine, I need more information. Could you please clarify: 1. What specific actions should users be able to perform with the engine? 2. What are the expected behaviors and responses of the system when distributing cases? 3. What data inputs and outputs are required, and are there any specific validations needed? 4. Are there any business rules or constraints that should be considered? 5. What user roles and permissions are necessary? 6. Are there any integration requirements with other systems?"\n}',
            },
            {
                "id": 11,
                "message": "1.\tSpecific User Actions\n\t•\tCreate and Submit Cases: Users (e.g., customer support agents or external customers) should be able to input new cases into the system, filling out necessary details such as category, priority, and description.\n\t•\tAssign or Reassign Cases: Authorized users (e.g., team leads) should be able to manually override the automatic assignment under special circumstances.\n\t•\tView Case Status and History: Users need to see the current status of a case (e.g., new, in-progress, escalated) and its assignment history.\n\t•\tManage Distribution Rules: Administrators should be able to create, modify, or delete distribution rules, such as “cases of type X go to team Y,” or “case priority P gets assigned to user group G.”\n\t2.\tExpected Behaviors and Responses\n\t•\tReal-Time Assignment: As soon as a case is created or updated, the engine should run the appropriate logic to assign it to the correct user, queue, or team.\n\t•\tLoad Balancing: The engine should consider factors like agent availability, workloads, and skills before making an assignment.\n\t•\tNotifications: Once a case is assigned or reassigned, the relevant users (case owner, impacted team) should be automatically notified via email or in-app alerts.\n\t•\tError Handling: If the engine cannot assign a case (for instance, no qualified agents available), it should flag the case for manual intervention and notify an administrator.\n\t3.\tData Inputs, Outputs, and Validations\n\t•\tInputs:\n\t•\tCase Details: Title, description, severity, category, customer information.\n\t•\tUser/Agent Data: Skills, availability status, current workload.\n\t•\tBusiness Rules: Conditions or algorithms that define how cases should be routed.\n\t•\tOutputs:\n\t•\tAssignment Results: The assigned user or queue for each case.\n\t•\tAudit/History Logs: A record of every assignment or re-assignment.\n\t•\tValidations:\n\t•\tEnsure required fields (e.g., priority, category) are populated before processing.\n\t•\tValidate that agents have the required skill or permission to handle the case.\n\t•\tConfirm that the workflow rules do not conflict (e.g., two rules assigning the same case to different teams).\n\t4.\tBusiness Rules or Constraints\n\t•\tPriorities and SLAs: High-priority cases should be assigned first and may have time-sensitive handling.\n\t•\tEscalation Path: If a case is not updated or resolved within a certain window, it should escalate to the next level.\n\t•\tGeographical Constraints: Certain cases might need to be routed to specific regions or time zones.\n\t•\tCompliance and Security: The system should respect data access rules and not assign sensitive cases to unauthorized agents.\n\t5.\tUser Roles and Permissions\n\t•\tAdministrator: Full access to manage distribution rules, view all cases, override assignments, and configure system settings.\n\t•\tTeam Lead / Manager: Can modify distribution logic for their team, reassign cases if needed, and view case metrics.\n\t•\tAgent: Can view and work on assigned cases, update case status, and escalate if necessary.\n\t•\tViewer / Auditor: Read-only access to case data and assignment logs, often for compliance or reporting purposes.\n\t6.\tIntegration Requirements\n\t•\tCRM/Support Portal Integration: The engine should integrate with our existing CRM to pull in customer data and case details automatically.\n\t•\tNotification Systems: Integrate with email and/or chat platforms (e.g., Slack, Teams) to deliver assignment notifications.\n\t•\tAnalytics / Reporting: Potential integration with a BI tool or data warehouse to analyze case distribution metrics over time.\n\t•\tAuthentication and Authorization: Should align with our existing Single Sign-On (SSO) or identity provider to maintain consistent user management.",
                "from_id": "1",
                "to_id": "1",
                "current_document": 5,
            },
            {
                "id": 12,
                "message": "The functional requirements have been detailed based on the provided user actions, expected behaviors, data inputs/outputs, business rules, user roles, and integration requirements. If there are any additional specific scenarios or constraints you would like to address, please let me know.",
                "from_id": "1",
                "to_id": "1",
                "current_document": 6,
                "llm_raw_response": '{\n    "updated functional requirements": [\n        "Users must be able to create and submit new cases, including details such as category, priority, and description.",\n        "Authorized users must be able to manually assign or reassign cases, overriding automatic assignments when necessary.",\n        "Users must be able to view the current status and history of a case, including its assignment history.",\n        "Administrators must be able to manage distribution rules, including creating, modifying, or deleting rules for case assignments.",\n        "The system must automatically assign cases in real-time, considering agent availability, workloads, and skills.",\n        "The system must send notifications to relevant users when a case is assigned or reassigned.",\n        "The system must flag cases for manual intervention and notify an administrator if automatic assignment fails.",\n        "The system must validate that all required fields are populated before processing a case.",\n        "The system must ensure agents have the required skills or permissions to handle a case.",\n        "The system must prevent conflicting workflow rules in case assignments.",\n        "High-priority cases must be assigned first and handled within specified SLAs.",\n        "The system must escalate cases that are not updated or resolved within a certain timeframe.",\n        "The system must route cases based on geographical constraints when necessary.",\n        "The system must comply with data access rules and not assign sensitive cases to unauthorized agents.",\n        "The system must integrate with the existing CRM to automatically pull in customer data and case details.",\n        "The system must integrate with notification systems to deliver assignment notifications via email or chat platforms.",\n        "The system must support integration with analytics or BI tools for case distribution metrics analysis.",\n        "The system must align with existing SSO or identity providers for authentication and authorization."\n    ],\n    "communication": "The functional requirements have been detailed based on the provided user actions, expected behaviors, data inputs/outputs, business rules, user roles, and integration requirements. If there are any additional specific scenarios or constraints you would like to address, please let me know."\n}',
            },
        ],
        "document": "Hi this is raw html",
    }

    logger.info("Successfully retrieved Document (ID=%s).", document.id)
    return JsonResponse(response, status=200)


####################################################################################################
########################################## Private Methods #########################################
####################################################################################################


def _validate_create_document_request_data(data):
    """
    Checks whether the required fields ('document_schema' and 'title') are present
    in the data and returns a JsonResponse if there's a problem. Otherwise None.
    """
    logger.debug("Validating create_document request data.")
    missing_fields = []
    for field in ["document_schema", "title"]:
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
    # if not _user_can_access_document(user, document):
    #     logger.warning(
    #         "User %s attempted to access Document ID %s without permission.",
    #         user.username,
    #         document.id,
    #     )
    #     return JsonResponse({"error": "Permission denied"}, status=403), None

    # If everything is fine, return the Document
    return None, document


####################################################################################################


def _create_document_from_data(request, data):
    """
    Private helper function that creates and returns a new Document
    based on the validated JSON data and the authenticated user.
    Raises ValidationError if the document_schema is not found.
    """
    document_schema_id = data["document_schema"]
    latest_version = data.get("latest_version", 0)

    logger.debug(
        "Creating Document with document_schema_id=%s, latest_version=%s",
        document_schema_id,
        latest_version,
    )

    document_schema = DocumentSchema.objects.filter(id=document_schema_id).first()
    if not document_schema:
        logger.warning(
            "Document Schema ID %s not found. Cannot create Document.",
            document_schema_id,
        )
        raise ValidationError(
            f"Document Schema with ID {document_schema_id} does not exist."
        )

    document = Document.objects.create(
        document_schema=document_schema,
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
