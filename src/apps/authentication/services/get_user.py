from src.apps.authentication.selectors import (
    get_user_by_id as get_user_by_id_selector,
    get_user_by_phone_number as get_user_id_selector
)

def get_user_by_id(user_id):
    return get_user_by_id_selector(user_id)

def get_user_id_by_phone_number(phone_number):
    user = get_user_id_selector(phone_number=phone_number)
    if user is None:
        return None
    return user.id
