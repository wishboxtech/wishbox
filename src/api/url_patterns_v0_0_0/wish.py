from django.urls import path

from src.api.views.wishlist import (
    CreateAnonymousFriendAPIView,
    GetWishByIdAPIView,
    SubmitRequestAPIView,
)

wish_urlpatterns = [
    path(
        "create-anonymous-friend/",
        CreateAnonymousFriendAPIView.as_view(),
        name="create_anonymous_friend",
    ),
    path("<str:id>/", GetWishByIdAPIView.as_view(), name="wish_by_id"),
    path("<str:id>/request/", SubmitRequestAPIView.as_view(), name="submit_request"),
]
