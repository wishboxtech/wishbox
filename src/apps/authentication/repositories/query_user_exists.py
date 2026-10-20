import uuid

from src.apps.authentication.models import User


def user_with_id_exist(user_id: str | uuid.UUID):
    return User.objects.filter(id=user_id).exists()
