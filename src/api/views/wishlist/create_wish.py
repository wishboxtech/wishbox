from rest_framework import status
from rest_framework.response import Response

from src.api.permissions import IsOwnerOfWishlist
from rest_framework.views import APIView

from src.apps.wishlist.services import create_wish
from src.utils.exceptions import BadRequestException


class CreateWishAPIVIew(APIView):
    permission_classes = [IsOwnerOfWishlist]

    def post(self, *args, **kwargs):
        wishlist_id = kwargs.get("id")
        profile_id = self.request.user.id

        obj = {"profile_id": profile_id, "wishlist_id": wishlist_id}
        self.check_object_permissions(self.request, obj)

        data = self.request.data
        data["wishlist"] = wishlist_id
        created, wish, errs = create_wish(
            data=data,
        )
        if errs:
            raise BadRequestException(
                message=errs.get("errors"),
                error_type=errs.get("error_type"),
            )
        return Response(
            data={
                "created": created,
                "data": wish,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
