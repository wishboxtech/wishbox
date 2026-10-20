from rest_framework.views import APIView
from rest_framework.response import Response
from src.api.serialization import input_dto
from src.core.composition import gifting_service
from src.apps.wishlist.dto.gifting import ReserveGiftInputDTO, ChangeGiftInputDTO
from src.api.views.wishlist.reserve.serializer import (
    ReserveInputSerializer,
    ChangeInputSerializer,
    OutputSerializer,
)
from src.utils.exceptions import BadRequestException


class ReserveGiftAPIView(APIView):
    permission_classes = []

    def post(self, request, **kwargs):
        actor = request.user.id if request.user.is_authenticated else None
        serializer = ReserveInputSerializer(
            data=request.data, context={"registered": actor is not None}
        )
        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.errors, error_type=list(serializer.errors)
            )
        result = gifting_service().reserve(
            ReserveGiftInputDTO(
                wish_id=kwargs["id"], profile_id=actor, **serializer.validated_data
            )
        )
        return Response(
            {"created": True, "data": OutputSerializer(result).data, "status": 201},
            status=201,
        )

    def patch(self, request, **kwargs):
        dto = input_dto(
            ChangeInputSerializer,
            request.data,
            ChangeGiftInputDTO,
            wish_id=kwargs["id"],
            profile_id=request.user.id if request.user.is_authenticated else None,
            token=request.headers.get("X-Wishy-Gift-Token", ""),
        )
        result = gifting_service().change(dto)
        return Response(
            {"ok": True, "data": OutputSerializer(result).data, "status": 200}
        )
