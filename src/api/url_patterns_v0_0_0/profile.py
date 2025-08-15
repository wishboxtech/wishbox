from django.urls import path
from src.api.views.profile import ProfileAPIView, WishlistAPIView, UpdateWishlist

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
        "wishlist/<str:id>/",
        UpdateWishlist.as_view(),
        name="wishlist_with_id",
    ),
]
