from rest_framework import serializers
from src.api.serialization import DTOResponseSerializer


class OutputSerializer(DTOResponseSerializer):
    """Serialize the use-case result."""


class ReadInputSerializer(serializers.Serializer):
    notification_id = serializers.UUIDField(required=False, allow_null=True)
