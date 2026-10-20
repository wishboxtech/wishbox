from rest_framework import serializers

from src.api.serialization import DTOResponseSerializer


class CreateWishlistInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    description = serializers.CharField()
    cover = serializers.UUIDField(required=False, allow_null=True)


class WishlistOutputSerializer(DTOResponseSerializer):
    """Serialize created wishlists and wishlist list items."""
