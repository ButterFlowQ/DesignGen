from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Additional fields can be added here if needed
    pass


class Agent(models.Model):
    # Primary key for the Agent model
    id = models.AutoField(primary_key=True)
    # Name of the AI agent
    name = models.CharField(max_length=255)
    # Description of the AI agent
    description = models.TextField()

    def __str__(self):
        # String representation of the Agent object
        return f"Agent(id={self.id}, name={self.name}, description={str(self.description)[:20]}{'...' if len(self.description) > 20 else ''})"


class WorkflowElement(models.Model):
    # Primary key for the WorkflowElement model
    id = models.AutoField(primary_key=True)
    # Workflow ID associated with the element
    workflow_id = models.CharField(max_length=255)
    # Position of the element in the workflow
    position = models.IntegerField()
    # Agent ID associated with the element
    agent_id = models.CharField(max_length=255)
    # Name of the workflow element
    name = models.CharField(max_length=255)
    # Description of the workflow element
    description = models.TextField()
    # Prompt for relevancy checking
    relevancy_checking_prompt = models.TextField()

    def __str__(self):
        # String representation of the WorkflowElement object
        return (
            f"WorkflowElement(id={self.id}, "
            f"workflow_id={self.workflow_id}, "
            f"position={self.position}, "
            f"agent_id={self.agent_id}, "
            f"name={self.name}, "
            f"description={str(self.description)[:20]}..., "
            f"relevancy_checking_prompt={str(self.relevancy_checking_prompt)[:20]}...)"
            if len(self.relevancy_checking_prompt) > 20
            else f"relevancy_checking_prompt={self.relevancy_checking_prompt})"
        )


# Workflow model
class Workflow(models.Model):
    # Primary key for the Workflow model
    id = models.AutoField(primary_key=True)
    # Name of the workflow
    name = models.CharField(max_length=255)
    # Description of the workflow
    description = models.TextField()

    def __str__(self):
        # String representation of the Workflow object
        return (
            f"Workflow(id={self.id}, "
            f"name={self.name}, "
            f"description={str(self.description)[:20]}{'...' if len(self.description) > 20 else ''})"
        )


class Document(models.Model):
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
    # Owner of the document
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # String representation of the Document object
        return (
            f"Document(id={self.id}, "
            f"title={self.title}, "
            f"creation_time={self.creation_time}, "
            f"version={self.version}, "
            f"workflow_elements={str(self.workflow_elements)[:20]}"
            f"{'...' if len(str(self.workflow_elements)) > 20 else ''}, "
            f"owner={self.owner.username if self.owner else 'N/A'})"
        )


class ChatMessage(models.Model):
    # Choices for agent type
    AGENT_TYPE_CHOICES = [
        ("agent", "Agent"),
        ("user", "User"),
    ]

    # Primary key for the Chat model
    id = models.AutoField(primary_key=True)
    # Document ID associated with the chat
    doc_id = models.CharField(max_length=255)
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
    # Current document content
    current_document = models.TextField()
    # Type of the agent receiving the message (agent or user)
    to_agent_type = models.CharField(max_length=5, choices=AGENT_TYPE_CHOICES)
    # ID of the agent receiving the message
    to_id = models.CharField(max_length=255)
    # Start position in the document
    start_position = models.IntegerField()
    # End position in the document
    end_position = models.IntegerField()
    # Current workflow element ID
    current_workflow_element = models.IntegerField()

    def __str__(self):
        # String representation of the Chat object
        return (
            f"Chat(id={self.id}, "
            f"doc_id={self.doc_id}, "
            f"from_agent_type={self.from_agent_type}, "
            f"from_id={self.from_id}, "
            f"in_reply_to={self.in_reply_to}, "
            f"creation_time={self.creation_time}, "
            f"message={str(self.message)[:20]}{'...' if len(self.message) > 20 else ''}, "
            f"current_document={str(self.current_document)[:20]}..., "
            f"to_agent_type={self.to_agent_type}, "
            f"to_id={self.to_id}, "
            f"start_position={self.start_position}, "
            f"end_position={self.end_position}, "
            f"current_workflow_element={self.current_workflow_element})"
        )
