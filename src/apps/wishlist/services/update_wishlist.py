from src.apps.wishlist.selectors import get_wishlist_by_id
from src.apps.wishlist.serializers import EditWishlistSerialzier, WishlistSerializer
from src.static import SerializerErrors
from src.utils.exceptions import InvalidWishlistId


def update_wishlist(id, data):
    """
    Update a wishlist based on the provided data
    """
    errs = {}
    updated = False
    wishlist_data = None

    error_dict = SerializerErrors.CreateWishlist.errors
    wishlist = get_wishlist_by_id(id)
    if not wishlist:
        raise InvalidWishlistId()

    serializer = EditWishlistSerialzier(
        instance=wishlist,
        data=data,
        partial=True,
    )
    if serializer.is_valid():
        data = serializer.save()
        updated = True
        wishlist_data = WishlistSerializer(instance=data, many=False).data
    else:
        error_types = []
        errors = serializer.errors
        for error in errors.keys():
            error_type = error_dict.get(error)
            error_types.append(error_type)
        errs["errors"] = errors
        errs["error_type"] = error_types
    return updated, wishlist_data, errs
