from rest_framework.views import APIView
from rest_framework.response import Response
from src.api.serialization import input_dto
from src.api.views.wishlist.experience.serializer import (
    ExperienceInputSerializer,
    ExperienceOutputSerializer,
)
from src.apps.wishlist.dto.gifting import GiftExperienceInputDTO, SaveExperienceInputDTO
from src.core.composition import gifting_service


class GiftExperienceAPIView(APIView):
    permission_classes = []

    def actor(self, request, id):
        return {
            "reservation_id": id,
            "profile_id": request.user.id if request.user.is_authenticated else None,
            "token": request.headers.get("X-Wishy-Gift-Token", ""),
        }

    def get(self, request, id):
        result = gifting_service().experience(
            GiftExperienceInputDTO(**self.actor(request, id))
        )
        return Response(
            {"ok": True, "data": ExperienceOutputSerializer(result).data, "status": 200}
        )

    def patch(self, request, id):
        dto = input_dto(
            ExperienceInputSerializer,
            request.data,
            SaveExperienceInputDTO,
            **self.actor(request, id)
        )
        result = gifting_service().save_experience(dto)
        return Response(
            {"ok": True, "data": ExperienceOutputSerializer(result).data, "status": 200}
        )
