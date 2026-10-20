from rest_framework import serializers

from src.api.serialization import DTOResponseSerializer


class UpsertProfileInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=150, required=False, allow_null=True, allow_blank=True
    )
    last_name = serializers.CharField(
        max_length=150, required=False, allow_null=True, allow_blank=True
    )
    birthdate = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=("male", "female", ""), required=False, allow_null=True
    )
    bio = serializers.CharField(
        max_length=250, required=False, allow_null=True, allow_blank=True
    )
    photo = serializers.UUIDField(required=False, allow_null=True)
    cat_avatar = serializers.JSONField(required=False, allow_null=True)


class ProfileOutputSerializer(DTOResponseSerializer):
    """Serialize profile data for both GET and PUT responses."""
