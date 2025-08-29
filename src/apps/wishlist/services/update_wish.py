from src.apps.wishlist.serializers import EditWishSerialzier, WishSerializer
from src.apps.wishlist.selectors import get_wish_by_id, is_owner_of_wishlist
from src.static import SerializerErrors
from src.utils.exceptions import InvalidWishId, NotWishlistOwner


def update_wish(id, data, profile_id):
    """
    Update a wish based on the provided data
    """
    errs = {}
    updated = False
    wish_data = None

    error_dict = SerializerErrors.CreateWishlist.errors
    wish = get_wish_by_id(id)
    if not wish:
        raise InvalidWishId()

    if data.get("wishlist") and not is_owner_of_wishlist(
        data.get("wishlist"),
        profile_id,
    ):
        raise NotWishlistOwner()

    serializer = EditWishSerialzier(
        instance=wish,
        data=data,
        partial=True,
    )

    if serializer.is_valid():
        data = serializer.save()
        updated = True
        wish_data = WishSerializer(instance=data, many=False).data
    else:
        error_types = []
        errors = serializer.errors
        for error in errors.keys():
            error_type = error_dict.get(error)
            error_types.append(error_type)
        errs["errors"] = errors
        errs["error_type"] = error_types
    return updated, wish_data, errs
