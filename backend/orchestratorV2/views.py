import json
import logging

from agents.agent_factory import AgentFactory
from agents.types import AgentType, LLMResponse

from django.db import transaction
from django.db.models import Max
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Document,
    VersionedDocument,
    ChatMessage,
    Conversation,
    DocumentElement,
    DocumentSchema,
)
from .serializers import (
    DocumentCreateSerializer,
    DocumentListSerializer,
    RevertDocumentSerializer,
    ChatMessageCreateSerializer,
    ChatMessageSerializer,
)

logger = logging.getLogger(__name__)


##############################################################################
#                         1) DocumentListCreateView                          #
##############################################################################


class DocumentListCreateView(APIView):
    """
    - GET /documents/:
         Returns a paginated list of the user's Documents with minimal info:
           { "id", "title", "last_modified" }
         'title' and 'last_modified' come from the latest *active* version.

    - POST /documents/:
         Creates a new Document + initial VersionedDocument.
         Expects JSON: { "title": <str>, "latest_version": <int, optional> }
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request, *args, **kwargs):
        docs_qs = Document.objects.filter(owner=request.user)

        # Build a list of dicts => {id, title, last_modified} from the latest active version
        doc_list = []
        for doc in docs_qs:
            latest_active_vdoc = (
                VersionedDocument.objects.filter(document=doc, is_deleted=False)
                .order_by("-version")
                .first()
            )
            if latest_active_vdoc:
                doc_list.append(
                    {
                        "id": doc.id,
                        "title": latest_active_vdoc.title,
                        "last_modified": latest_active_vdoc.creation_time,
                    }
                )
            # If no active version, skip or handle accordingly

        # Paginate the resulting list
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set an appropriate page size
        paginated_data = paginator.paginate_queryset(doc_list, request, view=self)

        # Optionally serialize them with a DRF serializer,
        # but here we might just return the raw dictionaries:
        return paginator.get_paginated_response(paginated_data)

    def post(self, request, *args, **kwargs):
        logger.info("Creating a new Document + initial VersionedDocument.")

        serializer = DocumentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        title = data["title"]
        latest_version = data.get("latest_version", 1)

        try:
            with transaction.atomic():
                doc = Document.objects.create(
                    owner=request.user,
                    latest_version=latest_version,
                    document_schema=DocumentSchema.objects.get(
                        pk=data["document_schema_id"]
                    ),
                )
                vdoc = VersionedDocument.objects.create(
                    document=doc,
                    version=latest_version,
                    title=title,
                    document_elements={},
                    html_document={},
                    is_deleted=False,
                )
        except Exception as e:
            logger.error("Error creating Document: %s", e)
            return Response(
                {"error": "Failed to create document"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "document_id": doc.id,
                "versioned_document_id": vdoc.id,
            },
            status=status.HTTP_201_CREATED,
        )


##############################################################################
#                        2) DocumentRetrieveView (new)                       #
##############################################################################


class DocumentRetrieveView(APIView):
    """
    GET /documents/<int:doc_id>/:
      Returns detailed info for a single Document + the latest *active* version:
      {
         "id": <int>,
         "latest_version": <int>,
         "title": <str>,
         "version": <int>,
         "document_elements": {...},
         "html_elements":{...},
         "creation_time": <datetime>,
         "":
         ...
      }
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request, doc_id=None, *args, **kwargs):
        if not doc_id:
            return Response(
                {"error": "Document ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        doc = get_object_or_404(Document, pk=doc_id, owner=request.user)

        latest_active_vdoc = (
            VersionedDocument.objects.filter(document=doc, is_deleted=False)
            .order_by("-version")
            .first()
        )
        if not latest_active_vdoc:
            return Response(
                {"error": "No active version found."}, status=status.HTTP_404_NOT_FOUND
            )

        data = {
            "id": doc.id,
            "latest_version": doc.latest_version,
            "title": latest_active_vdoc.title,
            "version": latest_active_vdoc.version,
            "document_elements": latest_active_vdoc.document_elements,
            "html_elements": latest_active_vdoc.html_document,
            "creation_time": latest_active_vdoc.creation_time,
            "conversation_id": doc.current_conversation_id,
        }
        return Response(data, status=status.HTTP_200_OK)


##############################################################################
#                           3) DocumentRevertView                            #
##############################################################################


class DocumentRevertView(APIView):
    """
    POST /documents/<int:doc_id>/revert/
    JSON body:
    {
      "target_version": <int>
    }
    Steps:
     - Mark current VersionedDocument as is_deleted=True
     - Mark all ChatMessages referencing that version as is_deleted=True
       => If a conversation ends up with all messages deleted => delete it
     - Un-delete (or ensure) the target_version is the new active version
     - doc.latest_version = target_version
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    @transaction.atomic
    def post(self, request, doc_id=None, *args, **kwargs):
        if not doc_id:
            return Response(
                {"error": "Document ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        document = get_object_or_404(Document, pk=doc_id, owner=request.user)

        serializer = RevertDocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        target_version = serializer.validated_data["target_version"]

        # 1) Mark the current version as deleted
        current_vdoc = VersionedDocument.objects.filter(
            document=document, version=document.latest_version, is_deleted=False
        ).first()

        if not current_vdoc:
            return Response(
                {"error": "Current version is not active or not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        current_vdoc.is_deleted = True
        current_vdoc.save()

        # 2) Mark all ChatMessages referencing current_vdoc as deleted
        messages_qs = ChatMessage.objects.filter(
            current_document=current_vdoc, is_deleted=False
        )
        messages_qs.update(is_deleted=True)

        # 3) Potentially delete any conversations with no remaining active messages
        conversation_ids = messages_qs.values_list(
            "conversation_id", flat=True
        ).distinct()
        for convo_id in conversation_ids:
            if convo_id:
                convo = Conversation.objects.filter(pk=convo_id).first()
                if convo:
                    has_active_msgs = ChatMessage.objects.filter(
                        conversation=convo, is_deleted=False
                    ).exists()
                    if not has_active_msgs:
                        # Hard-delete or soft-delete the conversation
                        convo.delete()

        # 4) Un-delete target_version, if needed
        target_vdoc = VersionedDocument.objects.filter(
            document=document, version=target_version
        ).first()
        if not target_vdoc:
            return Response(
                {"error": f"Version {target_version} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if target_vdoc.is_deleted:
            target_vdoc.is_deleted = False
            target_vdoc.save()

        # 5) Update doc.latest_version
        document.latest_version = target_version
        document.save()

        return Response(
            {"message": f"Document reverted to version {target_version}."},
            status=status.HTTP_200_OK,
        )


##############################################################################
#                              4) ChatMessageView                            #
##############################################################################


class ChatMessageListCreateView(generics.ListCreateAPIView):
    """
    A single endpoint for listing AND creating chat messages.

    GET /chat/messages/?conversation_id=<int>
      => Paginates all ChatMessages for that conversation, returning them as JSON.

    POST /chat/messages/
      => Create a user ChatMessage, call LLM, create an agent response message,
         update the Document with a new VersionedDocument. Returns both messages.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer  # used for listing
    pagination_class = PageNumberPagination
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        """
        Restrict the queryset to a single conversation if conversation_id is provided.
        Also exclude any 'is_deleted' messages if you use soft delete.
        """
        conversation_id = self.request.query_params.get("conversation_id")
        document_id = self.request.query_params.get("document_id")
        qs = ChatMessage.objects.all()

        # Example: exclude soft-deleted messages if your model has is_deleted
        qs = qs.filter(is_deleted=False)

        if conversation_id:
            qs = qs.filter(
                document_id=document_id,
                conversation_id=conversation_id,
            )
        else:
            # Possibly return an empty queryset, or all messages, or raise an error
            qs = qs.none()
        return qs.order_by("creation_time")

    def list(self, request, *args, **kwargs):
        """
        Overriding list() is optional if you just want the default DRF pagination response.
        By default, ListCreateAPIView calls get_queryset() + self.get_serializer().
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Override create() to implement:
          1) Validate user data (using ChatMessageCreateSerializer)
          2) Create a user ChatMessage
          3) Call the LLM => update doc => create agent message
          4) Return both messages in the response
        """
        serializer = ChatMessageCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data

        # 1) Create the user chat message
        user_msg = self._create_user_chat_message(request, validated)

        # 2) Process with LLM => new version => agent msg
        agent_msg = self._process_llm_response(user_msg, request)

        # 3) Return both messages in the response
        # We can use ChatMessageSerializer or just build the response dict
        user_msg_data = ChatMessageSerializer(user_msg).data
        agent_msg_data = ChatMessageSerializer(agent_msg).data
        return Response(
            {"user_message": user_msg_data, "agent_message": agent_msg_data},
            status=status.HTTP_201_CREATED,
        )

    def _create_user_chat_message(self, request, data):
        """
        Creates the user's ChatMessage and (if needed) the Conversation.
        """
        document_id = data["document_id"]
        document = get_object_or_404(Document, pk=document_id, owner=request.user)

        conversation_id = data.get("conversation_id")
        if conversation_id:
            conversation = get_object_or_404(Conversation, pk=conversation_id)
        else:
            conversation = Conversation.objects.create(document=document)
            document.current_conversation = conversation
            document.save()

        # current active version
        latest_vdoc = VersionedDocument.objects.filter(
            document=document, version=document.latest_version, is_deleted=False
        ).first()
        if not latest_vdoc:
            raise ValueError("No active version found for the Document.")

        user_msg = ChatMessage.objects.create(
            document=document,
            conversation=conversation,
            current_document=latest_vdoc,
            message=data["message"],
            to_id=data["to_id"],
            from_id=str(request.user.id),
            is_user_message=True,
        )
        return user_msg

    @transaction.atomic
    def _process_llm_response(self, user_msg, request):
        """
        - Gather chat history
        - Identify doc element => call LLM
        - Create new doc version => create agent ChatMessage
        """
        # 1) Chat history
        conversation = user_msg.conversation
        chat_history = ChatMessage.objects.filter(
            conversation=conversation, is_deleted=False
        ).order_by("creation_time")

        # 2) LLM call
        document_element = get_object_or_404(DocumentElement, pk=user_msg.to_id)
        llm_response = AgentFactory.create_agent(
            AgentType[document_element.type]
        ).process(chat_history)
        logger.debug("LLM response: %s", llm_response)

        # 3) Create new doc version & agent message
        return self._handle_llm_response(
            llm_response, user_msg.document, document_element, request, conversation
        )

    def _handle_llm_response(
        self, llm_response, document, document_element, request, conversation
    ):
        """
        Example method to create a new version of the Document
        based on the maximum version ever used, so we don't overwrite
        a previously-existing version number.
        """
        # 1) Find the maximum version number used by this doc (including deleted)
        current_version = document.latest_version
        max_version = (
            VersionedDocument.objects.filter(document=document).aggregate(
                Max("version")
            )["version__max"]
            or 0
        )
        new_version_number = max_version + 1

        # 2) Update the Document's 'latest_version'
        document.latest_version = new_version_number
        document.save()

        # 3) Get the 'previous' version doc
        prev_version_doc = VersionedDocument.objects.filter(
            document=document, version=current_version
        ).first()
        if not prev_version_doc:
            # Fallback if no previous version found; handle accordingly
            # (e.g. if the doc only has version=1 so far).
            raise ValueError(
                f"No 'previous' VersionedDocument found for doc {document.id} version {max_version}"
            )

        # 4) Create the new VersionedDocument
        new_vdoc = VersionedDocument.objects.create(
            document=document,
            version=new_version_number,
            title=prev_version_doc.title,
            document_elements=dict(prev_version_doc.document_elements),
            html_document=dict(prev_version_doc.html_document),
            is_deleted=False,
        )

        # 5) Update doc elements / handle LLM response
        updated_content = llm_response.get("updated_doc_element")
        if updated_content is not None:
            new_vdoc.document_elements[document_element.name] = updated_content
        if "html" in llm_response:
            new_vdoc.html_document[document_element.name] = llm_response["html"]
        new_vdoc.save()

        # 6) Create agent ChatMessage referencing this new version
        agent_msg = ChatMessage.objects.create(
            document=document,
            conversation=conversation,
            current_document=new_vdoc,
            message=llm_response.get("response_message", "No LLM response"),
            from_id=str(document_element.id),
            to_id=str(request.user.id),
            is_user_message=False,
            llm_raw_response=llm_response.get("raw_response", ""),
        )
        logger.info(
            f"Created agent message #{agent_msg.id}, doc {document.id}, new version {new_version_number}"
        )
        return agent_msg
