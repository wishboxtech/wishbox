from datetime import datetime, timedelta

import jwt
from django.core.cache import cache
from django.utils import timezone

from settings import ACCESS_TTL, JWT_SECRET, REFRESH_TTL
from src.apps.authentication.selectors import user_with_id_exist
from src.utils.exceptions import InvalidRefresh


def gen_token(data):
    return jwt.encode(payload=data, key=JWT_SECRET, algorithm="HS512")


def __gen_tokens(user_id, extra_data):
    extra_data = (
        extra_data
        if extra_data is not None
        else {"patental_control": False, "selected_age": None}
    )
    data = {
        "user_id": user_id,
        "created_at": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "access",
        "extra_data": extra_data,
    }
    access_token = gen_token(data=data)
    data["type"] = "refresh"
    data["access"] = access_token
    refresh_token = gen_token(data=data)
    cache.set(access_token, "", timeout=ACCESS_TTL)
    cache.set(refresh_token, "", timeout=REFRESH_TTL * 60)
    return access_token, refresh_token


def login(user, extra_data=None):
    access_token, refresh_token = __gen_tokens(
        user_id=str(user.id), extra_data=extra_data
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


def claim_token(token):
    return jwt.decode(jwt=token, key=JWT_SECRET, algorithms=["HS512"])


def __has_keys(data: dict, *keys):
    return all([i in data.keys() for i in keys])


def validate_token(token, check_time=True):
    if cache.ttl(token) == 0:
        return False
    try:
        data = claim_token(token)
    except Exception:
        return False
    if "type" not in data.keys():
        return False
    delta = timedelta(seconds=ACCESS_TTL)
    if data.get("type") == "refresh":
        if not __has_keys(
            data, "user_id", "created_at", "type", "access", "extra_data"
        ):
            return False
        access = data.get("access")
        if not validate_token(access, check_time=False):
            return False
        delta = timedelta(minutes=REFRESH_TTL)
    elif data.get("type") != "access" or not __has_keys(
        data, "user_id", "created_at", "type", "extra_data"
    ):
        return False
    user_id = data.get("user_id")
    if not user_with_id_exist(user_id):
        return False
    data_created_at_str = data.get("created_at")
    data_created_at_unaware = datetime.strptime(
        data_created_at_str, "%Y-%m-%d %H:%M:%S"
    )
    data_created_at = timezone.make_aware(data_created_at_unaware)
    if check_time and timezone.now() > data_created_at + delta:
        return False
    return True


def refresh(token, extra_data=None):
    if not validate_token(token):
        raise InvalidRefresh()
    jwt_data = claim_token(token)
    if jwt_data.get("type") != "refresh":
        raise InvalidRefresh()
    cache.expire(token, timeout=0)
    data_access = jwt_data.get("access")
    cache.expire(data_access, timeout=10)
    if extra_data is None:
        extra_data = jwt_data.get("extra_data")
    user_id = jwt_data.get("user_id")
    return __gen_tokens(user_id=user_id, extra_data=extra_data)
