from rest_framework import serializers

from src.apps.profile.models import Profile
from src.apps.storage.services import serialize_media


class ReadProfileSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField(read_only=True)
    phone_number = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    is_phone_number_verified = serializers.SerializerMethodField(read_only=True)
    has_accepted_terms = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "profile_id",
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "birthdate",
            "gender",
            # "is_user_completed",
            "is_phone_number_verified",
            "has_accepted_terms",
            "bio",
            "photo",
        )

    def get_photo(self, obj):
        if obj.photo is None:
            return None
        return serialize_media(media=obj.photo)

    def get_phone_number(self, obj):
        if obj.phone_number is None:
            return None
        return obj.phone_number

    def get_email(self, obj):
        if obj.email is None:
            return None
        return obj.email

    def get_is_phone_number_verified(self, obj):
        if obj.is_phone_number_verified is None:
            return None
        return obj.is_phone_number_verified

    def get_has_accepted_terms(self, obj):
        if obj.has_accepted_terms is None:
            return None
        return obj.has_accepted_terms


class WriteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "profile",
            "first_name",
            "last_name",
            "birthdate",
            "bio",
            "gender",
            "photo",
        )
