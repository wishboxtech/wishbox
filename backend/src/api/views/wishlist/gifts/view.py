from rest_framework.views import APIView
from rest_framework.response import Response
from src.api.serialization import input_dto
from src.core.composition import gifting_service
from rest_framework.permissions import IsAuthenticated
from src.apps.wishlist.dto.gifting import InboxInputDTO
from src.api.views.wishlist.gifts.serializer import OutputSerializer


class MyGiftsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = gifting_service().gifts(InboxInputDTO(profile_id=request.user.id))
        return Response(
            {
                "ok": True,
                "data": OutputSerializer(result, many=True).data,
                "status": 200,
            }
        )
