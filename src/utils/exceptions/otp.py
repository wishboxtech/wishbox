from django.utils.translation import gettext as _

from src.static import ErrorEnum
from src.utils.exceptions.general import BadRequestException


class InvalidOTP(Exception):
    pass


class InvalidRefresh(BadRequestException):
    error_type = [ErrorEnum.RefreshToken.TOKEN_IS_NOT_VALID]
    message = {"refresh_token": _("refresh_token is invalid.")}

    def __init__(self):
        pass
