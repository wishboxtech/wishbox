from django.urls import path

from src.api.views.profile.avatar.view import AvatarAPIView
from src.api.views.profile.profile.view import ProfileAPIView
from src.api.views.wishlist.wishlist.view import WishlistAPIView

profile_urlpatterns = [
    path(
        "",
        ProfileAPIView.as_view(),
        name="profile",
    ),
    path(
        "wishlist/",
        WishlistAPIView.as_view(),
        name="wishlist",
    ),
    path(
        "avatar/",
        AvatarAPIView.as_view(),
        name="avatar",
    ),
]
