from django.urls import path

from src.api.views.wishlist import GetWishByIdAPIView

wish_urlpatterns = [
    path("<str:id>/", GetWishByIdAPIView.as_view(), name="wish_by_id"),
]
