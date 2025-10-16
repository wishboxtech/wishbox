from rest_framework import serializers

from src.apps.storage.services import serialize_media
from src.apps.wishlist.models import Wish


class WishSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Wish
        fields = (
            "id",
            "name",
            "description",
            "price",
            "cover",
            "created_at",
            "updated_at",
        )

    def get_cover(self, obj):
        if obj.cover is None:
            return None
        return serialize_media(media=obj.cover)


class WriteWishSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ("wishlist", "name", "description", "cover", "price")


class EditWishSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ("wishlist", "name", "description", "cover", "price")
