from django.urls import path

from .views import document
from .views import workflow

# Document APIS
urlpatterns = [
    path("create_document/", document.create_document, name="create_document"),
    path("get_document/", document.get_document, name="get_document"),
]

# Workflow APIS
urlpatterns += [
    path("send_chat_message/", workflow.send_chat_message, name="send_chat_message"),
    path("get_chat_message/", workflow.send_chat_message, name="get_chat_message"),
]
