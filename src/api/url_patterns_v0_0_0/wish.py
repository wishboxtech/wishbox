from django.urls import path

from src.api.views.wishlist.create_anonymous_friend.view import (
    CreateAnonymousFriendAPIView,
)
from src.api.views.wishlist.get_wish_by_id.view import GetWishByIdAPIView
from src.api.views.wishlist.submit_request.view import SubmitRequestAPIView

wish_urlpatterns = [
    path(
        "create-anonymous-friend/",
        CreateAnonymousFriendAPIView.as_view(),
        name="create_anonymous_friend",
    ),
    path("<str:id>/", GetWishByIdAPIView.as_view(), name="wish_by_id"),
    path("<str:id>/request/", SubmitRequestAPIView.as_view(), name="submit_request"),
]
