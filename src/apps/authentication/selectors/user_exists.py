import uuid
from typing import Union

from src.apps.authentication.models import User


def user_with_id_exist(user_id: Union[str, uuid.UUID]):
    return User.objects.filter(id=user_id).exists()
