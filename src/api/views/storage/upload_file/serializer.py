from rest_framework import serializers

from src.api.serialization import DTOResponseSerializer


class UploadMediaInputSerializer(serializers.Serializer):
    file = serializers.FileField()


class UploadMediaOutputSerializer(DTOResponseSerializer):
    """Serialize the uploaded media identifier."""
