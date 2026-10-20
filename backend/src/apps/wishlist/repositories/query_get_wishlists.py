import uuid
from typing import Union

from src.apps.wishlist.models import Wishlist


def get_wishlists_by_profile(profile_id: Union[str, uuid.UUID]):
    return (
        Wishlist.objects.only(
            "id",
            "name",
            "description",
            "cover",
        )
        .filter(profile_id=profile_id)
        .select_related("cover")
    )


def get_wishlist_by_id(id: Union[str, uuid.UUID]):
    try:
        return Wishlist.objects.only(
            "id",
            "name",
            "description",
            "cover",
        ).get(id=id)
    except Wishlist.DoesNotExist:
        return None
