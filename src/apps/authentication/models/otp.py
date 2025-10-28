import json
import uuid

from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from settings import OTP_TTL
from src.static import ErrorEnum
from src.utils.exceptions import BadRequestException, InvalidOTP
from src.utils.otp import generate_otp


class OneTimePassword:
    code = None
    otp_id = None
    target = None

    def __init__(
        self,
        state,
        phone_number=None,
        email=None,
        prefix="",
    ):
        self.otp_id = str(uuid.uuid4())
        self.target = phone_number if phone_number else email
        self.state = state
        self.code = generate_otp()
        self.prefix = prefix
        self.created_at = timezone.now()
        self.__save()

    def __save(self):
        key = f"{self.prefix}{self.otp_id}"
        target_key = f"{self.prefix}{self.target}"
        not_duplicate = cache.set(target_key, "", timeout=OTP_TTL, nx=True)
        if not not_duplicate:
            raise BadRequestException(
                message={"message": _("OTP already sent.")},
                error_type=[ErrorEnum.SendOneTimePassword.OTP_ALREADY_SENT],
            )
        cache.set(key, self.__gen_value(), timeout=OTP_TTL)

    def __gen_value(self):
        raw_code = "{}{}".format(self.otp_id, self.code)
        raw_data = {
            "user_target": self.target,
            "state": self.state,
            "hash": make_password(raw_code),
        }
        return json.dumps(raw_data)

    def verify_otp(otp_id, otp_code, prefix=""):
        key = f"{prefix}{otp_id}"
        if cache.get(key) is None:
            raise InvalidOTP("otp is inavlid")
        value = cache.get(key)
        data = json.loads(value)
        if not check_password("{}{}".format(otp_id, otp_code), data.get("hash")):
            raise InvalidOTP("otp is inavlid")
        return data.get("user_target"), data.get("state")

    def otp_exist(target, prefix=""):
        key = f"{prefix}{target}"
        return cache.ttl(key) != 0

    @property
    def deadline(self):
        return self.created_at.timestamp() + OTP_TTL
