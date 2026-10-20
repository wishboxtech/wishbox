from rest_framework import serializers
from src.api.serialization import DTOResponseSerializer


class OutputSerializer(DTOResponseSerializer):
    """Serialize the use-case result."""


class SharedInputSerializer(serializers.Serializer):
    visitor = serializers.UUIDField()
