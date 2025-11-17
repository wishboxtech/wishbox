from src.apps.wishlist.serializers import WishlistSerializer, WriteWishlistSerialzier
from src.static import SerializerErrors


def create_wishlist(data):
    """
    Create a wishlist based on the provided data
    """
    errs = {}
    created = False
    wishlist_data = None

    error_dict = SerializerErrors.CreateWishlist.errors

    serializer = WriteWishlistSerialzier(
        data=data,
        partial=True,
    )
    if serializer.is_valid():
        data = serializer.save()
        created = True
        wishlist_data = WishlistSerializer(instance=data, many=False).data
    else:
        error_types = []
        errors = serializer.errors
        for error in errors.keys():
            error_type = error_dict.get(error)
            error_types.append(error_type)
        errs["errors"] = errors
        errs["error_type"] = error_types
    return created, wishlist_data, errs
