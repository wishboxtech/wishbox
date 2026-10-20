from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serialization import input_dto
from src.apps.wishlist.dto import CreateWishlistInputDTO, ListWishlistsInputDTO
from src.core.composition import wishlist_service
from src.static import SerializerErrors


from src.api.views.wishlist.wishlist.serializer import (
    CreateWishlistInputSerializer,
    WishlistOutputSerializer,
)


class WishlistAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    error_codes = SerializerErrors.CreateWishlist.errors

    def get(self, *args, **kwargs):
        user_id = self.request.user.id
        wishlists = wishlist_service().list_wishlists(
            ListWishlistsInputDTO(profile_id=user_id)
        )
        return Response(
            data={
                "ok": True,
                "data": WishlistOutputSerializer(wishlists, many=True).data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, *args, **kwargs):
        dto = input_dto(
            CreateWishlistInputSerializer,
            self.request.data,
            CreateWishlistInputDTO,
            error_codes=self.error_codes,
            aliases={"cover": "cover_id"},
            profile_id=self.request.user.id,
        )
        result = wishlist_service().create_wishlist(dto)
        return Response(
            {
                "created": True,
                "data": WishlistOutputSerializer(result).data,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
