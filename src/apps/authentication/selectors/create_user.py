from django.db import transaction

from src.apps.authentication.models import User


@transaction.atomic
def create_user(phone_number: str, **kwargs):
    return User.objects.create_user(phone_number=phone_number, **kwargs)
