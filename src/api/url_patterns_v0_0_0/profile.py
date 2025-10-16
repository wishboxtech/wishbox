from django.urls import path

from src.api.views.profile import ProfileAPIView
from src.api.views.wishlist import UpdateWishlistAPIView, WishlistAPIView

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
]
