from django.urls import path

from src.api.views.wishlist.wish_action.view import WishActionAPIView
from src.api.views.wishlist.wishlist_action.view import WishlistActionAPIView

wishlist_urlpatterns = [
    path("<str:id>/", WishlistActionAPIView.as_view(), name="wishlist_action"),
    path(
        "<str:id>/wish/<str:wishid>/", WishActionAPIView.as_view(), name="wish_action"
    ),
]
