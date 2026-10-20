from rest_framework import serializers

from src.api.serialization import DTOResponseSerializer


class CreateWishInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=0)
    cover = serializers.UUIDField(required=False, allow_null=True)


class UpdateWishlistInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, required=False)
    description = serializers.CharField(required=False)
    cover = serializers.UUIDField(required=False, allow_null=True)


class WishOutputSerializer(DTOResponseSerializer):
    """Serialize created wishes and wish list items."""


class WishlistOutputSerializer(DTOResponseSerializer):
    """Serialize the wishlist after PATCH."""


class DeleteWishlistOutputSerializer(DTOResponseSerializer):
    """Serialize the outcome of deleting a wishlist."""
