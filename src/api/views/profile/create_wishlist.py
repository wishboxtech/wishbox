from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from src.apps.wishlist.services import create_wishlist
from src.utils.exceptions import BadRequestException


class CreateWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        profile_id = self.request.user.id
        data = self.request.data
        data["profile"] = profile_id
        created, wishlist, errs = create_wishlist(
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
                "data": wishlist,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
