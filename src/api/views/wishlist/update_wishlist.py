from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from src.apps.wishlist.services import update_wishlist
from src.utils.exceptions import BadRequestException


class UpdateWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, *args, **kwargs):
        wishlist_id = kwargs.get("id")
        data = self.request.data

        try:
            updated, wishlist, errs = update_wishlist(
                wishlist_id,
                data,
            )
        except Exception as e:
            raise BadRequestException(
                message=e.message,
                error_type=e.error_type,
            )
        if errs:
            raise BadRequestException(
                message=errs.get("errors"),
                error_type=errs.get("error_type"),
            )
        return Response(
            data={
                "updated": updated,
                "data": wishlist,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
