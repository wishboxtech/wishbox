from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.wishlist.services import get_wishes_by_wishlist_id


class GetWishesAPIView(APIView):
    permission_classes = []

    def get(self, *args, **kwargs):
        wishlist_id = kwargs.get("id")
        wishes = get_wishes_by_wishlist_id(wishlist_id=wishlist_id)
        return Response(
            data={
                "ok": True,
                "data": wishes,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
