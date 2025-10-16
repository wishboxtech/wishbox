from django.db import transaction

from src.apps.authentication.selectors import create_user as create_user_selector


@transaction.atomic
def create_user(phone_number, **kwargs):
    done = False
    user_id = None
    err = None
    try:
        user = create_user_selector(phone_number=phone_number, **kwargs)
        done = True
        user_id = user.id
    except Exception as e:
        err = str(e)
    return done, user_id, err
