from django.urls import path

from .views.document import create_document, get_document
from .views.workflow import send_chat_message, get_chat_message

# Document APIS
urlpatterns = [
    path("create_document/", create_document, name="create_document"),
    path("get_document/", get_document, name="get_document"),
]

# Workflow APIS
urlpatterns += [
    path("send_chat_message/", send_chat_message, name="send_chat_message"),
    path("get_chat_message/", get_chat_message, name="get_chat_message"),
]
