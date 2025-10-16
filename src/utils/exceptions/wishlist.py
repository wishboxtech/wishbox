from django.utils.translation import gettext_lazy as _

from src.static.error_enum import ErrorEnum
from src.utils.exceptions import BadRequestException


class InvalidWishlistId(BadRequestException):
    error_type = [ErrorEnum.Wishlist.WISHLIST_NOT_FOUND]
    message = {"error": _("wishlist_id is invalid.")}

    def __init__(self):
        pass


class InvalidWishId(BadRequestException):
    error_type = [ErrorEnum.Wishlist.WISH_NOT_FOUND]
    message = {"error": _("wish_id is invalid.")}

    def __init__(self):
        pass


class NotWishlistOwner(BadRequestException):
    error_type = [ErrorEnum.Wishlist.NOT_WISHLIST_OWNER]
    message = {"error": _("you are not a wishlist owner.")}

    def __init__(self):
        pass
