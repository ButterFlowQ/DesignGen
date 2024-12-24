from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Additional fields can be added here if needed
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="workflowmanager_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="workflowmanager_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


class Agent(models.Model):
    # Primary key for the Agent model
    id = models.AutoField(primary_key=True)
    # Name of the AI agent
    name = models.CharField(max_length=255)
    # Description of the AI agent
    description = models.TextField()


# Workflow model
class Workflow(models.Model):
    # Primary key for the Workflow model
    id = models.AutoField(primary_key=True)
    # Name of the workflow
    name = models.CharField(max_length=255)
    # Description of the workflow
    description = models.TextField()


class WorkflowElement(models.Model):
    # Primary key for the WorkflowElement model
    id = models.AutoField(primary_key=True)
    # Workflow ID associated with the element
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    # Position of the element in the workflow
    position = models.IntegerField()
    # Agent ID associated with the element
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    # Name of the workflow element
    name = models.CharField(max_length=255)
    # Description of the workflow element
    description = models.TextField()
    # Prompt for relevancy checking
    relevancy_checking_prompt = models.TextField()


class Document(models.Model):
    # Primary key for the Document model
    id = models.AutoField(primary_key=True)
    # Version of the document
    latest_version = models.IntegerField()
    # Workflow associated with the document
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    # Owner of the document
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class VersionedDocument(models.Model):
    # Primary key for the Document model
    id = models.AutoField(primary_key=True)
    # Title of the document
    title = models.CharField(max_length=255)
    # Timestamp when the document was created
    creation_time = models.DateTimeField(auto_now_add=True)
    # Version of the document
    version = models.IntegerField()
    # Mapping of workflow element ID to corresponding document content
    workflow_elements = models.JSONField()
    # Foreign key to the Document model
    document = models.ForeignKey(Document, on_delete=models.CASCADE)


class ChatMessage(models.Model):
    # Choices for agent type
    AGENT_TYPE_CHOICES = [
        ("agent", "Agent"),
        ("user", "User"),
    ]

    # Primary key for the Chat model
    id = models.AutoField(primary_key=True)
    # Document ID associated with the chat
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    # Type of the agent sending the message (agent or user)
    from_agent_type = models.CharField(max_length=5, choices=AGENT_TYPE_CHOICES)
    # ID of the agent sending the message
    from_id = models.CharField(max_length=255)
    # ID of the message this message is replying to (optional)
    in_reply_to = models.CharField(max_length=255, null=True, blank=True)
    # Timestamp when the message was created
    creation_time = models.DateTimeField(auto_now_add=True)
    # Content of the message
    message = models.TextField()
    # Foreign key to the VersionedDocument model
    current_document = models.ForeignKey(VersionedDocument, on_delete=models.CASCADE)
    # Type of the agent receiving the message (agent or user)
    to_agent_type = models.CharField(max_length=5, choices=AGENT_TYPE_CHOICES)
    # ID of the agent receiving the message
    to_id = models.CharField(max_length=255)
    # Start position in the document
    start_position = models.IntegerField()
    # End position in the document
    end_position = models.IntegerField()
    # Current workflow element ID
    current_workflow_element = models.ForeignKey(
        WorkflowElement, on_delete=models.CASCADE
    )
