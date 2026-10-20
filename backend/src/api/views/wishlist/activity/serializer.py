from rest_framework import serializers
from src.api.serialization import DTOResponseSerializer


class OutputSerializer(DTOResponseSerializer):
    """Serialize the use-case result."""


class ActivityInputSerializer(serializers.Serializer):
    visitor = serializers.UUIDField()
    action = serializers.ChoiceField(choices=["view", "like", "unlike"], required=False)


class ActivityActionInputSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["view", "like", "unlike"])
