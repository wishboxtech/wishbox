from rest_framework import serializers

from src.api.serialization import DTOResponseSerializer


class SubmitRequestInputSerializer(serializers.Serializer):
    friend = serializers.UUIDField(required=False, allow_null=True)
    anonymous_friend = serializers.UUIDField(required=False, allow_null=True)


class ReservationOutputSerializer(DTOResponseSerializer):
    """Serialize the reservation created by this endpoint."""
