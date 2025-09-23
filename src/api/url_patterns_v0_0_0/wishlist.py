from django.urls import path
from src.api.views.wishlist import WishAPIView, UpdateWishAPIView

wishlist_urlpatterns = [
    path("<str:id>/", WishAPIView.as_view(), name="wish"),
    path(
        "<str:id>/wish/<str:wishid>/", UpdateWishAPIView.as_view(), name="update_wish"
    ),
]
