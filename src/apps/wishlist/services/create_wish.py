from src.apps.wishlist.serializers import WriteWishSerialzier, WishSerializer
from src.static import SerializerErrors


def create_wish(data):
    """
    Create a wish based on the provided data
    """
    errs = {}
    created = False
    wish_data = None

    error_dict = SerializerErrors.CreateWish.errors

    serializer = WriteWishSerialzier(
        data=data,
        partial=True,
    )
    if serializer.is_valid():
        data = serializer.save()
        created = True
        wish_data = WishSerializer(instance=data, many=False).data
    else:
        error_types = []
        errors = serializer.errors
        for error in errors.keys():
            error_type = error_dict.get(error)
            error_types.append(error_type)
        errs["errors"] = errors
        errs["error_type"] = error_types
    return created, wish_data, errs
