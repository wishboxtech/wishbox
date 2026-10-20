from django.urls import path

from src.api.views.wishlist.wish_action.view import WishActionAPIView
from src.api.views.wishlist.wishlist_action.view import WishlistActionAPIView

from src.api.views.wishlist.shared.view import SharedListAPIView

wishlist_urlpatterns = [
    path("<uuid:id>/shared/", SharedListAPIView.as_view(), name="shared_wishlist"),
    path("<str:id>/", WishlistActionAPIView.as_view(), name="wishlist_action"),
    path(
        "<str:id>/wish/<str:wishid>/", WishActionAPIView.as_view(), name="wish_action"
    ),
]
