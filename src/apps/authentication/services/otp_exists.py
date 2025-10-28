from src.apps.authentication.models import OneTimePassword


def one_time_password_exists(target, prefix=""):
    return OneTimePassword.otp_exist(target=target, prefix=prefix)
