from rest_framework import serializers

from src.api.serialization import DTOResponseSerializer


class SendOTPInputSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(r"^09\d{9}$", required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)


class SendOTPOutputSerializer(DTOResponseSerializer):
    """Serialize the OTP identifier returned by the use case."""
