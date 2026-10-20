from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serialization import input_dto
from src.apps.wishlist.dto import UpdateWishInputDTO, WishActorInputDTO
from src.core.composition import wishlist_service
from src.static import ErrorEnum, SerializerErrors
from src.utils.exceptions import NotFoundException


from src.api.views.wishlist.wish_action.serializer import (
    UpdateWishInputSerializer,
    WishOutputSerializer,
    DeleteWishOutputSerializer,
)


class WishActionAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    error_codes = SerializerErrors.CreateWish.errors

    def patch(self, *args, **kwargs):
        dto = input_dto(
            UpdateWishInputSerializer,
            self.request.data,
            UpdateWishInputDTO,
            error_codes=self.error_codes,
            aliases={"cover": "cover_id"},
            id=kwargs["wishid"],
            wishlist_id=kwargs["id"],
            profile_id=self.request.user.id,
        )
        result = wishlist_service().update_wish(dto)
        return Response(
            {
                "updated": True,
                "data": WishOutputSerializer(result).data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, *args, **kwargs):
        dto = WishActorInputDTO(
            id=kwargs["wishid"],
            wishlist_id=kwargs["id"],
            profile_id=self.request.user.id,
        )
        result = wishlist_service().delete_wish(dto)
        if not result.deleted:
            raise NotFoundException(
                message={"error": "wish does not exist"},
                error_type=[ErrorEnum.Wishlist.WISH_NOT_FOUND],
            )
        return Response(
            {**DeleteWishOutputSerializer(result).data, "status": status.HTTP_200_OK}
        )
