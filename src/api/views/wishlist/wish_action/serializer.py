from rest_framework import serializers

from src.api.serialization import DTOResponseSerializer


class UpdateWishInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, required=False)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=0, required=False)
    cover = serializers.UUIDField(required=False, allow_null=True)


class WishOutputSerializer(DTOResponseSerializer):
    """Serialize the wish after PATCH."""


class DeleteWishOutputSerializer(DTOResponseSerializer):
    """Serialize the outcome of deleting a wish."""
