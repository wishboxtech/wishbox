from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.core.composition import wishlist_service
from src.shared.dto import IdInputDTO
from src.static import ErrorEnum
from src.utils.exceptions import NotFoundException

from src.api.views.wishlist.get_wish_by_id.serializer import WishOutputSerializer


class GetWishByIdAPIView(APIView):
    permission_classes = []

    def get(self, *args, **kwargs):
        wish_id = kwargs.get("id")

        wish = wishlist_service().get_wish(IdInputDTO(id=wish_id))
        if not wish:
            raise NotFoundException(
                error_type=[ErrorEnum.Wishlist.WISH_NOT_FOUND],
                message={"error": _("wish does not exist")},
            )

        return Response(
            data={
                "ok": True,
                "data": WishOutputSerializer(wish).data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
