from src.apps.authentication.models import OneTimePassword
from src.utils.exceptions import InvalidOTP


def verify_otp_and_get_user_phone(otp_id, otp_code, prefix=""):
    try:
        user_target, state = OneTimePassword.verify_otp(
            otp_id=otp_id, otp_code=otp_code, prefix=""
        )
        return user_target, state
    except InvalidOTP:
        return None, None
