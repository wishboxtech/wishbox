from src.utils.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response
from src.api.serialization import input_dto
from src.core.composition import gifting_service
from src.apps.wishlist.dto.gifting import ActivityInputDTO
from src.api.views.wishlist.activity.serializer import (
    ActivityInputSerializer,
    ActivityActionInputSerializer,
    OutputSerializer,
)


class WishActivityAPIView(APIView):
    permission_classes = []

    def execute(self, action=None):
        data = {"visitor": self.request.headers.get("X-Wishy-Visitor")}
        if action is not None:
            data["action"] = action
        dto = input_dto(
            ActivityInputSerializer,
            data,
            ActivityInputDTO,
            wish_id=self.kwargs["id"],
            profile_id=self.request.user.id
            if self.request.user.is_authenticated
            else None,
            token=self.request.headers.get("X-Wishy-Gift-Token", ""),
        )
        result = gifting_service().activity(dto)
        return Response(
            {"ok": True, "data": OutputSerializer(result).data, "status": 200}
        )

    def get(self, request, **kwargs):
        return self.execute()

    def post(self, request, **kwargs):
        serializer = ActivityActionInputSerializer(data=request.data)
        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.errors, error_type=list(serializer.errors)
            )
        return self.execute(serializer.validated_data["action"])
