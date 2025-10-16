from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.wishlist.services import get_wish_by_id
from src.static import ErrorEnum
from src.utils.exceptions import NotFoundException


class GetWishByIdAPIView(APIView):
    permission_classes = []

    def get(self, *args, **kwargs):
        wish_id = kwargs.get("id")

        wish = get_wish_by_id(id=wish_id)
        if not wish:
            raise NotFoundException(
                error_type=[ErrorEnum.Wishlist.WISH_NOT_FOUND],
                message={"error": _("wish does not exist")},
            )

        return Response(
            data={
                "ok": True,
                "data": wish,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
