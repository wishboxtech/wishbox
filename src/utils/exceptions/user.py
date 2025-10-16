from django.utils.translation import gettext as _

from src.static.error_enum import ErrorEnum
from src.utils.exceptions import BadRequestException


class InvalidUserID(BadRequestException):
    error_type = [ErrorEnum.Services.INVALID_USER_ID]
    message = {"user_id": _("user_id is invalid.")}

    def __init__(self):
        pass