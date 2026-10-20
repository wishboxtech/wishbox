from django.urls import path

from src.api.views.wishlist.create_anonymous_friend.view import (
    CreateAnonymousFriendAPIView,
)
from src.api.views.wishlist.get_wish_by_id.view import GetWishByIdAPIView
from src.api.views.wishlist.reserve.view import ReserveGiftAPIView
from src.api.views.wishlist.activity.view import WishActivityAPIView

wish_urlpatterns = [
    path("<uuid:id>/activity/", WishActivityAPIView.as_view(), name="wish_activity"),
    path(
        "<uuid:id>/reservation/", ReserveGiftAPIView.as_view(), name="wish_reservation"
    ),
    path(
        "create-anonymous-friend/",
        CreateAnonymousFriendAPIView.as_view(),
        name="create_anonymous_friend",
    ),
    path("<str:id>/", GetWishByIdAPIView.as_view(), name="wish_by_id"),
    path("<str:id>/request/", ReserveGiftAPIView.as_view(), name="submit_request"),
]
