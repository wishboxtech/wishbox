import uuid
from typing import Union

from src.apps.wishlist.models import Wish


def delete_wish_by_id(id: Union[str, uuid.UUID]) -> bool:
    try:
        wish = Wish.objects.get(id=id)
        wish.delete()
        return True
    except Wish.DoesNotExist:
        return False
