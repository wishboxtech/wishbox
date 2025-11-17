import uuid
from typing import Union

from src.apps.wishlist.models import AnonymousFriend


def get_anonymous_friend_by_id(anonymous_friend_id: Union[str, uuid.UUID]):
    try:
        return AnonymousFriend.objects.only("id", "nickname").get(
            id=anonymous_friend_id
        )
    except AnonymousFriend.DoesNotExist:
        return None
