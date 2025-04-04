from django.db import models
from django.contrib.auth.models import User


class DocumentSchema(models.Model):
    """
    Represents different parts of a document (WorkflowElements) that
    define what a document is composed of.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Document schema"
        verbose_name_plural = "Document schemas"
        ordering = ["name"]


class DocumentElement(models.Model):
    """
    Represents a single part of a DocumentSchema. Each element is associated with:
    - A specific DocumentSchema
    - A position within that DocumentSchema
    """

    document_schema = models.ForeignKey(DocumentSchema, on_delete=models.CASCADE)
    position = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (Position {self.position})"

    class Meta:
        verbose_name = "Document element"
        verbose_name_plural = "Document elements"
        ordering = ["document_schema", "position"]


class Conversation(models.Model):
    """
    Represents a conversation between a user and the agent.
    """

    document = models.ForeignKey("Document", on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ["document"]


class Document(models.Model):
    """
    Represents a document that follows a defined workflow
    and tracks its current version number.
    """

    latest_version = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    current_conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_document",
    )
    document_schema = models.ForeignKey(DocumentSchema, on_delete=models.CASCADE)
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
    document_elements = models.JSONField(null=True, blank=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    html_document = models.JSONField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} (Version {self.version})"

    class Meta:
        verbose_name = "Versioned document"
        verbose_name_plural = "Versioned documents"
        ordering = ["document", "-version"]


class ChatMessage(models.Model):
    """
    Represents a single chat message associated with a Document.
    Messages can be sent by a user or an agent.
    """

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, null=True, blank=True
    )
    creation_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_user_message = models.BooleanField(default=False)
    from_id = models.CharField(max_length=255, null=True, blank=True)
    to_id = models.CharField(max_length=255, null=True, blank=True)
    current_document = models.ForeignKey(
        VersionedDocument, on_delete=models.CASCADE, null=True, blank=True
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, null=True, blank=True
    )
    llm_raw_response = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"ChatMessage #{self.pk} from {self.from_id} ({self.to_id})"

    class Meta:
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
        ordering = ["creation_time"]
