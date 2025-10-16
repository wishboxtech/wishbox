from src.apps.authentication.functions import login
from src.apps.authentication.selectors import get_user_by_id


def login_user_by_id(user_id, extra_data=None):
    user = get_user_by_id(user_id=user_id)
    if user is None:
        return None
    return login(user=user, extra_data=extra_data)
