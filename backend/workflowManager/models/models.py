from django.db import models
from django.contrib.auth.models import User


class Agent(models.Model):
    """
    Represents an AI agent that can perform automated tasks,
    such as generating or analyzing content within a workflow.
    """

    # If you need a custom primary key as a string, you can uncomment and use the following:
    # id = models.CharField(max_length=255, primary_key=True)

    # By default, Django will create 'id' as an AutoField primary key if you omit a custom one.

    type = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"
        ordering = ["type"]


class Workflow(models.Model):
    """
    Represents a sequence of steps (WorkflowElements) that
    define how a document should be processed or updated.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Workflow"
        verbose_name_plural = "Workflows"
        ordering = ["name"]


class WorkflowElement(models.Model):
    """
    Represents a single step in a Workflow. Each element is associated with:
    - A specific Workflow
    - A position within that Workflow
    - An Agent responsible for this step
    - A prompt for relevancy checking (if applicable)
    """

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    position = models.IntegerField()
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    json_key = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    relevancy_checking_prompt = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} (Position {self.position})"

    class Meta:
        verbose_name = "Workflow Element"
        verbose_name_plural = "Workflow Elements"
        ordering = ["workflow", "position"]


class Document(models.Model):
    """
    Represents a document that follows a defined workflow
    and tracks its current version number.
    """

    latest_version = models.IntegerField(default=1)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Document #{self.pk} owned by {self.owner.username}"

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ["pk"]


class VersionedDocument(models.Model):
    """
    Represents a saved version of a Document. Each new version
    can update or add content to the workflow elements.
    """

    title = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField()
    workflow_elements = models.JSONField(null=True, blank=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} (Version {self.version})"

    class Meta:
        verbose_name = "Versioned Document"
        verbose_name_plural = "Versioned Documents"
        ordering = ["document", "-version"]


class ChatMessage(models.Model):
    """
    Represents a single chat message associated with a Document.
    Messages can be sent by a user or an agent.
    """

    class AgentTypeChoices(models.TextChoices):
        AGENT = "agent", "Agent"
        USER = "user", "User"

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, null=True, blank=True
    )
    from_agent_type = models.CharField(
        max_length=5, choices=AgentTypeChoices.choices, null=True, blank=True
    )
    from_id = models.CharField(max_length=255, null=True, blank=True)
    in_reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )
    creation_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    current_document = models.ForeignKey(
        VersionedDocument, on_delete=models.CASCADE, null=True, blank=True
    )
    to_agent_type = models.CharField(
        max_length=5, choices=AgentTypeChoices.choices, null=True, blank=True
    )
    to_id = models.CharField(max_length=255, null=True, blank=True)
    start_position = models.IntegerField(null=True, blank=True)
    end_position = models.IntegerField(null=True, blank=True)
    current_workflow_element = models.ForeignKey(
        WorkflowElement, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"ChatMessage #{self.pk} from {self.from_agent_type} ({self.from_id})"

    class Meta:
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
        ordering = ["creation_time"]
