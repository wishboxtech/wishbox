from rest_framework import serializers

from src.api.serialization import DTOResponseSerializer


class UpdateAvatarInputSerializer(serializers.Serializer):
    changes = serializers.DictField()


class AvatarOutputSerializer(DTOResponseSerializer):
    """Serialize the rendered avatar returned by GET."""


class UpdateAvatarOutputSerializer(DTOResponseSerializer):
    """Serialize validated settings after a PATCH."""
