from settings import UNDER_DEVELOPMENT
from src.apps.authentication.models import OneTimePassword
from src.utils.otp import send_sms_otp


def create_one_time_password(state, phone_number=None, email=None, prefix=""):
    otp = OneTimePassword(
        phone_number=phone_number,
        email=email,
        prefix=prefix,
        state=state,
    )
    if not UNDER_DEVELOPMENT:
        send_sms_otp(phone=phone_number, otp=otp.code, deadline=otp.deadline)
    return otp.otp_id
