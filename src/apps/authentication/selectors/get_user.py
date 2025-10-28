import uuid
from typing import Union

from src.apps.authentication.models import User
from django.db.models import Q


def get_user_by_id(user_id: Union[str, uuid.UUID]):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def get_user_by_phone_number(phone_number: str):
    try:
        return User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return None


def get_user_by_email_or_phone(identifier: str):
    try:
        return User.objects.get(Q(phone_number=identifier) | Q(email=identifier))
    except User.DoesNotExist:
        return None
