from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serialization import input_dto
from src.apps.wishlist.dto import SubmitReservationInputDTO
from src.core.composition import wishlist_service
from src.static import SerializerErrors


from src.api.views.wishlist.submit_request.serializer import (
    SubmitRequestInputSerializer,
    ReservationOutputSerializer,
)


class SubmitRequestAPIView(APIView):
    # permission_classes = []
    error_codes = SerializerErrors.ReservationRequest.errors

    def post(self, *args, **kwargs):
        dto = input_dto(
            SubmitRequestInputSerializer,
            self.request.data,
            SubmitReservationInputDTO,
            error_codes=self.error_codes,
            aliases={"friend": "friend_id", "anonymous_friend": "anonymous_friend_id"},
            wish_id=kwargs["id"],
        )
        result = wishlist_service().submit_reservation(dto)
        return Response(
            {
                "created": True,
                "data": ReservationOutputSerializer(result).data,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
