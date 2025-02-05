from django.urls import path

from .views import (
    DocumentListCreateView,
    DocumentRetrieveView,
    DocumentRevertView,
    ChatMessageListCreateView,
)

urlpatterns = [
    # Documents
    path("documents/", DocumentListCreateView.as_view(), name="documents-list-create"),
    #   => GET /documents/   => list docs
    #   => POST /documents/  => create doc + version
    path(
        "documents/<int:doc_id>/",
        DocumentRetrieveView.as_view(),
        name="document-retrieve",
    ),
    #   => GET /documents/<doc_id>/  => get doc with latest version details
    path(
        "documents/<int:doc_id>/revert/",
        DocumentRevertView.as_view(),
        name="document-revert",
    ),
    #   => POST /documents/<doc_id>/revert/ => revert doc to older version
    # Chat
    path(
        "chat/messages/",
        ChatMessageListCreateView.as_view(),
        name="chat-messages-list-create",
    ),
    #   => POST /chat/messages/ => user sends msg => AI => new doc version
]
