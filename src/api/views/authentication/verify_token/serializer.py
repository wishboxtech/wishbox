from rest_framework import serializers

from src.api.serialization import DTOResponseSerializer


class VerifyOTPInputSerializer(serializers.Serializer):
    otp_id = serializers.CharField()
    otp_code = serializers.CharField()


class VerifyOTPOutputSerializer(DTOResponseSerializer):
    """Serialize the access and refresh tokens issued after verification."""
