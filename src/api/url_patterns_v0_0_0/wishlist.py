from django.urls import path

from src.api.views.wishlist import WishActionAPIView, WishlistActionAPIView

wishlist_urlpatterns = [
    path("<str:id>/", WishlistActionAPIView.as_view(), name="wishlist_action"),
    path(
        "<str:id>/wish/<str:wishid>/", WishActionAPIView.as_view(), name="wish_action"
    ),
]
