from rest_framework import serializers

from src.api.serialization import DTOResponseSerializer


class RefreshTokenInputSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class RefreshTokenOutputSerializer(DTOResponseSerializer):
    """Serialize the refreshed token pair."""
