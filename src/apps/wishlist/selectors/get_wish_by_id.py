import uuid
from typing import Union

from src.apps.wishlist.models import Wish


def get_wish_by_id(wish_id: Union[str, uuid.UUID]):
    try:
        return Wish.objects.only(
            "id",
            "name",
            "description",
            "price",
            "cover",
        ).get(id=wish_id)
    except Wish.DoesNotExist:
        return None
