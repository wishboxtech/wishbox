from src.apps.wishlist.serializers import WriteAnonymousFriendSerialzier
from src.static import SerializerErrors


def create_anonymous_friend(data):
    """
    Create an anonymous friend based on the provided data
    """

    errs = {}
    created = False
    anonymous_friend_id = None

    error_dict = SerializerErrors.CreateAnonymousFriend.errors

    serializer = WriteAnonymousFriendSerialzier(
        data=data,
    )

    if serializer.is_valid():
        instance = serializer.save()
        anonymous_friend_id = instance.id
        created = True
    else:
        error_types = []
        errors = serializer.errors
        for error in errors.keys():
            error_type = error_dict.get(error)
            error_types.append(error_type)
        errs["errors"] = errors
        errs["error_type"] = error_types
    return created, anonymous_friend_id, errs
