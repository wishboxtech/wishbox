import random

from settings import OTP_CODE_LENGTH


def generate_otp():
    random.seed(a=None, version=2)
    return "".join(random.choices("0123456789", k=OTP_CODE_LENGTH))
