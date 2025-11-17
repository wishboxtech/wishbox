from rest_framework.serializers import ModelSerializer, Serializer

from src.apps.profile.models import Avatar


class EditeAvatarSerializer(ModelSerializer):
    class Meta:
        model = Avatar
        fields = ("settings",)


class WriteAvatarSerializer(ModelSerializer):
    class Meta:
        model = Avatar
        fields = ("profile", "settings")
