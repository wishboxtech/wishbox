from rest_framework.views import APIView
from rest_framework.response import Response
from src.api.serialization import input_dto
from src.core.composition import gifting_service
from rest_framework.permissions import IsAuthenticated
from src.apps.wishlist.dto.gifting import InboxInputDTO
from src.api.views.wishlist.notifications.serializer import (
    ReadInputSerializer,
    OutputSerializer,
)


class NotificationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = gifting_service().inbox(InboxInputDTO(profile_id=request.user.id))
        return Response(
            {"ok": True, "data": OutputSerializer(result).data, "status": 200}
        )

    def patch(self, request):
        dto = input_dto(
            ReadInputSerializer, request.data, InboxInputDTO, profile_id=request.user.id
        )
        result = gifting_service().read_notifications(dto)
        return Response(
            {"ok": True, "data": OutputSerializer(result).data, "status": 200}
        )
