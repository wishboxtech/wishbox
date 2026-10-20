from src.api.views.wishlist.create_anonymous_friend.view import (
    CreateAnonymousFriendAPIView,
)
from src.api.views.wishlist.get_wish_by_id.view import GetWishByIdAPIView
from src.api.views.wishlist.submit_request.view import SubmitRequestAPIView
from src.api.views.wishlist.wish_action.view import WishActionAPIView
from src.api.views.wishlist.wishlist.view import WishlistAPIView
from src.api.views.wishlist.wishlist_action.view import WishlistActionAPIView

__all__ = [
    "CreateAnonymousFriendAPIView",
    "GetWishByIdAPIView",
    "SubmitRequestAPIView",
    "WishActionAPIView",
    "WishlistAPIView",
    "WishlistActionAPIView",
]
