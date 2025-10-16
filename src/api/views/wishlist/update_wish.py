from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.permissions import IsOwnerOfWishlist
from src.apps.wishlist.services import update_wish
from src.utils.exceptions import BadRequestException


class UpdateWishAPIView(APIView):
    permission_classes = [IsOwnerOfWishlist]

    def patch(self, *args, **kwargs):
        wishlist_id = kwargs.get("id")
        wish_id = kwargs.get("wishid")
        profile_id = self.request.user.id

        obj = {"profile_id": profile_id, "wishlist_id": wishlist_id}
        self.check_object_permissions(self.request, obj)
        data = self.request.data
        data["wishlist"] = wishlist_id

        try:
            updated, wishlist, errs = update_wish(
                wish_id,
                data,
                profile_id,
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
