import uuid
from typing import Union

from src.apps.wishlist.models import Wishlist


def delete_wishlist_by_id(id: Union[str, uuid.UUID]) -> bool:
    try:
        wish = Wishlist.objects.get(id=id)
        wish.delete()
        return True
    except Wishlist.DoesNotExist:
        return False
