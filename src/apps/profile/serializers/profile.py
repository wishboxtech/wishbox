from rest_framework import serializers

from src.apps.profile.models import Profile
from src.apps.storage.services import serialize_media

class ProfileSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "profile_id",
            "first_name",
            "last_name",
            "bio",
            "birthdate",
            "gender",
            "has_accepted_terms",
            "photo"
        )
    
    def get_photo(self, obj):
        if obj.photo is None:
            return None
        return serialize_media(media=obj.photo)