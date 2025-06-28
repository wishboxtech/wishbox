from src.apps.authentication.models import User
from src.apps.authentication.selectors import get_user_by_id
from src.utils.exceptions import InvalidUserID


def user_registered(user_id):
    try:
        user = get_user_by_id(user_id=user_id)
        if user.province is None or user.gender == "" or user.birth_date is None:
            return "sign_up"
        return "sign_in"
    except User.DoesNotExist:
        raise InvalidUserID()
