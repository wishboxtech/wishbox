import uuid
from typing import Union

from src.apps.wishlist.models import Wish


def get_wishes_by_wishlist_id(wishlist_id: Union[str, uuid.UUID]):
    return Wish.objects.only(
        "id",
        "name",
        "description",
        "price",
        "cover",
    ).filter(wishlist_id=wishlist_id)


def get_wish_by_id(id: Union[str, uuid.UUID]):
    try:
        return Wish.objects.only(
            "id",
            "name",
            "description",
            "cover",
        ).get(id=id)
    except Wish.DoesNotExist:
        return None
