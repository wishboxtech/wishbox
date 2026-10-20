from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serialization import input_dto
from src.apps.wishlist.dto import CreateAnonymousFriendInputDTO
from src.core.composition import wishlist_service
from src.static import SerializerErrors


from src.api.views.wishlist.create_anonymous_friend.serializer import (
    CreateAnonymousFriendInputSerializer,
    CreateAnonymousFriendOutputSerializer,
)


class CreateAnonymousFriendAPIView(APIView):
    # permission_classes = []
    error_codes = SerializerErrors.CreateAnonymousFriend.errors

    def post(self, *args, **kwargs):
        dto = input_dto(
            CreateAnonymousFriendInputSerializer,
            self.request.data,
            CreateAnonymousFriendInputDTO,
            error_codes=self.error_codes,
            aliases={},
        )
        result = wishlist_service().create_anonymous_friend(dto)
        return Response(
            {
                "created": True,
                **CreateAnonymousFriendOutputSerializer(result).data,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
