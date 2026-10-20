from rest_framework import serializers
from src.api.serialization import DTOResponseSerializer


class ExperienceInputSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=[
            "save_private",
            "share_thanks",
            "withdraw_thanks",
            "share_follow_up",
            "withdraw_follow_up",
            "acknowledge_follow_up",
        ]
    )
    fit = serializers.ChoiceField(
        choices=["fits", "adjust", "not_for_me", "trying"],
        required=False,
        allow_null=True,
    )
    private_note = serializers.CharField(
        max_length=800, allow_blank=True, required=False
    )
    follow_up_note = serializers.CharField(
        max_length=800, allow_blank=True, required=False
    )
    thank_you = serializers.CharField(max_length=800, allow_blank=True, required=False)


class ExperienceOutputSerializer(DTOResponseSerializer):
    """Recipient-only feedback or a giver-safe gift snapshot."""
