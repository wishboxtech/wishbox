from settings import UNDER_DEVELOPMENT
from src.apps.authentication.models import OneTimePassword

from src.utils.otp import send_sms_otp


def create_one_time_password(phone_number, prefix=""):
    otp = OneTimePassword(phone_number=phone_number, prefix=prefix)
    if not UNDER_DEVELOPMENT:
        send_sms_otp(phone=phone_number, otp=otp.code, deadline=otp.deadline)
    return otp.otp_id
