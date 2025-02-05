# serializers.py
from rest_framework import serializers
from orchestratorV2.models import ChatMessage


class DocumentCreateSerializer(serializers.Serializer):
    """
    Used by DocumentListCreateView (POST).
    """

    title = serializers.CharField(max_length=255)
    latest_version = serializers.IntegerField(required=False, min_value=0)
    document_schema_id = serializers.IntegerField()


class DocumentListSerializer(serializers.Serializer):
    """
    If you wanted to use a serializer for listing docs, you might do so,
    but in the example code we just return raw dictionaries.
    """

    id = serializers.IntegerField()
    title = serializers.CharField()
    last_modified = serializers.DateTimeField()


class RevertDocumentSerializer(serializers.Serializer):
    """
    Used by DocumentRevertView (POST).
    """

    target_version = serializers.IntegerField(min_value=1)


class ChatMessageCreateSerializer(serializers.Serializer):
    """
    For validating data when creating a new user ChatMessage.
    """

    message = serializers.CharField()
    document_id = serializers.IntegerField()
    to_id = serializers.CharField()
    conversation_id = serializers.IntegerField(required=False, allow_null=True)

    # If you need cross-field validation:
    def validate(self, attrs):
        # e.g. ensure 'message' isn't empty
        if not attrs["message"].strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return attrs


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    For listing or returning ChatMessage objects.
    """

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "message",
            "from_id",
            "to_id",
            "is_user_message",
            "creation_time",
            "llm_raw_response",
        ]
