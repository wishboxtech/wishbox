from django.utils.translation import gettext_lazy as _
from src.static.error_enum import ErrorEnum
from src.utils.exceptions import BadRequestException


class InvalidWishlistId(BadRequestException):
    error_type = [ErrorEnum.Services.INVALID_USER_ID]
    message = {"error": _("wishlist_id is invalid.")}

    def __init__(self):
        pass
