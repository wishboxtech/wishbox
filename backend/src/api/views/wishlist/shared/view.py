from rest_framework.views import APIView
from rest_framework.response import Response
from src.api.serialization import input_dto
from src.core.composition import gifting_service
from src.apps.wishlist.dto.gifting import SharedListInputDTO
from src.api.views.wishlist.shared.serializer import (
    SharedInputSerializer,
    OutputSerializer,
)


class SharedListAPIView(APIView):
    permission_classes = []

    def get(self, request, **kwargs):
        dto = input_dto(
            SharedInputSerializer,
            {"visitor": request.headers.get("X-Wishy-Visitor")},
            SharedListInputDTO,
            wishlist_id=kwargs["id"],
            profile_id=request.user.id if request.user.is_authenticated else None,
        )
        result = gifting_service().shared_list(dto)
        return Response(
            {"ok": True, "data": OutputSerializer(result).data, "status": 200}
        )
