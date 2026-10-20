from rest_framework import serializers
from src.api.serialization import DTOResponseSerializer


class OutputSerializer(DTOResponseSerializer):
    """Serialize the use-case result."""


class ReserveInputSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=150, required=False)
    guest_key = serializers.RegexField(r"^[a-f0-9]{64}$", required=False)
    purchase_by = serializers.DateField()
    purchase_plan = serializers.CharField(min_length=3, max_length=160)
    details_checked = serializers.BooleanField()

    def validate(self, attrs):
        if any(
            key in self.initial_data
            for key in ("friend", "anonymous_friend", "profile_id", "friend_id")
        ):
            raise serializers.ValidationError(
                "Identity comes from your session. Guests should supply a nickname."
            )
        if not self.context.get("registered") and not attrs.get("nickname"):
            raise serializers.ValidationError(
                {"nickname": "Tell us your name to reserve this gift."}
            )
        return attrs


class ChangeInputSerializer(serializers.Serializer):
    purchase_by = serializers.DateField(required=False, allow_null=True)
    action = serializers.ChoiceField(
        choices=["purchase", "cancel", "receive", "reschedule"]
    )
