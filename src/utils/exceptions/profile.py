from django.utils.translation import gettext_lazy as _

from src.static.error_enum import ErrorEnum
from src.utils.exceptions import BadRequestException


class InvalidAvatarSettings(BadRequestException):
    error_type = [ErrorEnum.Profile.INVALID_AVATAR_SETTINGS]
    message = {"error": _("avatar settings is invalid.")}

    def __init__(self):
        pass


class AvatarNotFound(BadRequestException):
    error_type = [ErrorEnum.Profile.AVATAR_NOT_FOUND]
    message = {"error": _("avatar settings not found.")}

    def __init__(self):
        pass
