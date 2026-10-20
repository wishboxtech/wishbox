from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serialization import input_dto
from src.apps.profile.dto import UpdateAvatarInputDTO
from src.core.composition import profile_service
from src.shared.dto import IdInputDTO
from src.static import ErrorEnum
from src.utils.exceptions import NotFoundException


from src.api.views.profile.avatar.serializer import (
    UpdateAvatarInputSerializer,
    AvatarOutputSerializer,
    UpdateAvatarOutputSerializer,
)


class AvatarAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        profile_id = self.request.user.id
        avatar = profile_service().get_avatar(IdInputDTO(id=profile_id))
        if avatar is None:
            raise NotFoundException(
                error_type=[ErrorEnum.Profile.AVATAR_NOT_FOUND],
                message={"error": _("avatar does not exist")},
            )

        return Response(
            data={
                "ok": True,
                "data": AvatarOutputSerializer(avatar).data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, *args, **kwargs):
        dto = input_dto(
            UpdateAvatarInputSerializer,
            {"changes": self.request.data},
            UpdateAvatarInputDTO,
            profile_id=self.request.user.id,
        )
        result = profile_service().update_avatar(dto)
        return Response(
            {
                "updated": True,
                "data": UpdateAvatarOutputSerializer(result).data["settings"],
                "status": status.HTTP_200_OK,
            }
        )
