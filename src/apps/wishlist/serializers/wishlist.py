from rest_framework import serializers

from src.apps.storage.services import serialize_media
from src.apps.wishlist.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Wishlist
        fields = (
            "id",
            "name",
            "description",
            "cover",
            "created_at",
            "updated_at",
        )

    def get_cover(self, obj):
        if obj.cover is None:
            return None
        return serialize_media(media=obj.cover)


class WriteWishlistSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ("profile", "name", "description", "cover")


class EditWishlistSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ("name", "description", "cover")
