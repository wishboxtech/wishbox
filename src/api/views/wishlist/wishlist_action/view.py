from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serialization import input_dto
from src.apps.wishlist.dto import (
    CreateWishInputDTO,
    ListWishesInputDTO,
    UpdateWishlistInputDTO,
    WishlistActorInputDTO,
)
from src.core.composition import wishlist_service
from src.static import ErrorEnum, SerializerErrors
from src.utils.exceptions import NotFoundException


from src.api.views.wishlist.wishlist_action.serializer import (
    CreateWishInputSerializer,
    UpdateWishlistInputSerializer,
    WishOutputSerializer,
    WishlistOutputSerializer,
    DeleteWishlistOutputSerializer,
)


class WishlistActionAPIView(APIView):
    permission_classes = ()
    error_codes = SerializerErrors.CreateWish.errors

    def get_permissions(self):
        if self.request.method in ("POST", "PATCH", "DELETE"):
            return [IsAuthenticated()]
        return super().get_permissions()

    def get(self, *args, **kwargs):
        wishlist_id = kwargs.get("id")
        wishes = wishlist_service().list_wishes(
            ListWishesInputDTO(wishlist_id=wishlist_id)
        )
        return Response(
            data={
                "ok": True,
                "data": WishOutputSerializer(wishes, many=True).data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, *args, **kwargs):
        dto = input_dto(
            CreateWishInputSerializer,
            self.request.data,
            CreateWishInputDTO,
            error_codes=self.error_codes,
            aliases={"cover": "cover_id"},
            wishlist_id=kwargs["id"],
            profile_id=self.request.user.id,
        )
        result = wishlist_service().create_wish(dto)
        return Response(
            {
                "created": True,
                "data": WishOutputSerializer(result).data,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )

    def patch(self, *args, **kwargs):
        dto = input_dto(
            UpdateWishlistInputSerializer,
            self.request.data,
            UpdateWishlistInputDTO,
            error_codes=self.error_codes,
            aliases={"cover": "cover_id"},
            id=kwargs["id"],
            profile_id=self.request.user.id,
        )
        result = wishlist_service().update_wishlist(dto)
        return Response(
            {
                "updated": True,
                "data": WishlistOutputSerializer(result).data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, *args, **kwargs):
        dto = WishlistActorInputDTO(id=kwargs["id"], profile_id=self.request.user.id)
        result = wishlist_service().delete_wishlist(dto)
        if not result.deleted:
            raise NotFoundException(
                message={"error": "wishlist does not exist"},
                error_type=[ErrorEnum.Wishlist.WISHLIST_NOT_FOUND],
            )
        return Response(
            {
                **DeleteWishlistOutputSerializer(result).data,
                "status": status.HTTP_200_OK,
            }
        )
