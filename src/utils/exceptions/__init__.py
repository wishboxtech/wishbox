from src.utils.exceptions.general import (
    BadRequestException,
    NotFoundException,
    Unauthorized,
)
from src.utils.exceptions.otp import InvalidOTP, InvalidRefresh
from src.utils.exceptions.user import InvalidUserID
from src.utils.exceptions.wishlist import (
    InvalidWishId,
    InvalidWishlistId,
    NotWishlistOwner,
)
