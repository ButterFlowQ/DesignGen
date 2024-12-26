import json

from agents.agent_factory import AgentFactory
from agents.types import AgentType, LLMResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import *


# Create your views here.
@csrf_exempt
def create_document(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    data = json.loads(request.body)
    document = Document.objects.create(
        workflow=Workflow.objects.filter(id=data["workflow"]).first(),
        owner=request.user,
        latest_version=data["latest_version"],
    )
    versioned_document = VersionedDocument.objects.create(
        document=document, title=data["title"], version=0
    )
    return JsonResponse(
        {"id": document.id, "versioned_document_id": versioned_document.id}
    )


@csrf_exempt
def send_chat_message(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    data = json.loads(request.body)
    chat_message = ChatMessage.objects.create(
        message=data["message"],
        document=Document.objects.filter(id=data["document_id"]).first(),
    )
    process_chat_message(chat_message, request)
    return JsonResponse(
        create_json_response(list(fetch_chat_messages(chat_message.document))),
        safe=False,
    )


def fetch_chat_messages(document):
    return ChatMessage.objects.filter(document=document)


def create_json_response(chat_messages):
    response = []
    for chat_message in chat_messages:
        response += [
            {
                "id": chat_message.id,
                "message": chat_message.message,
                "from_agent_type": chat_message.from_agent_type,
                "from_id": chat_message.from_id,
                "to_agent_type": chat_message.to_agent_type,
                "to_id": chat_message.to_id,
                "current_document": (
                    None
                    if chat_message.current_document is None
                    else chat_message.current_document.id
                ),
            }
        ]
    return response


def process_chat_message(chat_message, request):
    assign_workflow_element(chat_message)
    chat_message.save()
    document = chat_message.document
    chat_messages = fetch_chat_messages(document)
    llmresponse = AgentFactory.create_agent(
        AgentType[chat_message.current_workflow_element.agent.id]
    ).process(chat_messages)
    new_chat_message = handle_llm_response(
        llmresponse, document, chat_message.current_workflow_element, request
    )
    if llmresponse["move_to_next_workflow"]:
        process_chat_message(new_chat_message, request)


def handle_llm_response(
    llmresponse: LLMResponse,
    document: Document,
    workflow_element: WorkflowElement,
    request,
):
    updated_content = llmresponse["updated_workflow_doc"]
    document.latest_version += 1
    prevoius_version_document = VersionedDocument.objects.filter(
        document=document
    ).latest("version")
    latest_version_document = prevoius_version_document
    latest_version_document.version = document.latest_version
    if latest_version_document.workflow_elements is None:
        latest_version_document.workflow_elements = {}
    latest_version_document.workflow_elements[workflow_element.id] = updated_content
    latest_version_document.id = None
    latest_version_document.save()
    document.save()
    chat_message = ChatMessage.objects.create(
        document=document,
        message=llmresponse["response_message"],
        from_agent_type=AgentType[workflow_element.agent.id],
        from_id=workflow_element.agent.id,
        to_id=request.user.id,
        to_agent_type=AgentType.USER,
        current_document=latest_version_document,
    )
    chat_message.save()
    if llmresponse["move_to_next_workflow"]:
        document.workflow = document.workflow.next_workflow
        document.save()
    return chat_message


def assign_workflow_element(chat_message):
    document = chat_message.document
    chat_messages = fetch_chat_messages(document)
    workflow = document.workflow
    workflow_elements = WorkflowElement.objects.filter(workflow=workflow)
    chat_message.current_workflow_element = get_workflow_element(
        document, chat_message, chat_messages, workflow_elements
    )
    chat_message.to_agent_type = AgentType[
        chat_message.current_workflow_element.agent.id
    ]
    chat_message.to_id = chat_message.current_workflow_element.agent.id


def get_workflow_element(document, chat_message, chat_messages, workflow_elements):
    return workflow_elements[0]
