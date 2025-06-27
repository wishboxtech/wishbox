import uuid
from typing import Union

from src.apps.authentication.models import User


def get_user_by_id(user_id: Union[str, uuid.UUID]):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
