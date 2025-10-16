from rest_framework import serializers

from src.apps.wishlist.models import AnonymousFriend
from src.static.serializer_errors import SerializerErrors


class WriteAnonymousFriendSerialzier(serializers.ModelSerializer):
    class Meta:
        model = AnonymousFriend
        fields = ("nickname",)

    def validate_nickname(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                SerializerErrors.CreateAnonymousFriend.errors["nickname"]
            )
        return value
