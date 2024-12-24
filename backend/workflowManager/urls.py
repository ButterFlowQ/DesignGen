from django.urls import path
from . import views

urlpatterns = [
    path("create_document/", views.create_document, name="create_document"),
    path("send_chat_message/", views.send_chat_message, name="send_chat_message"),
    # Add more paths here as needed
]
