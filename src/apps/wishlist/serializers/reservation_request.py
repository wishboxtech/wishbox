from rest_framework import serializers

from src.apps.wishlist.models import ReservationRequest
from src.static import SerializerErrors


class WriteReservationRequestSerialzier(serializers.ModelSerializer):
    class Meta:
        model = ReservationRequest
        fields = (
            "wish",
            "anonymous_friend",
            "friend",
        )

    def validate(self, data):
        """
        Enforce business logic:
        - 'wish' is required.
        - at least one of ('friend', 'anonymous_friend') must exist.
        """
        error_dict = SerializerErrors.ReservationRequest.errors
        errors = {}

        wish = data.get("wish")
        friend = data.get("friend")
        anonymous_friend = data.get("anonymous_friend")

        if not wish:
            errors["wish"] = error_dict["wish"]

        if not friend and not anonymous_friend:
            errors["friend"] = error_dict["friend"]
            errors["anonymous_friend"] = error_dict["anonymous_friend"]

        if errors:
            raise serializers.ValidationError(errors)

        return data


class ReservationRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReservationRequest
        fields = (
            "wish",
            "anonymous_friend",
            "friend",
            "status",
            "created_at"
        )