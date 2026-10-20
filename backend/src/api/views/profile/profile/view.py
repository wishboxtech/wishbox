from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serialization import input_dto
from src.apps.profile.dto import UpsertProfileInputDTO
from src.core.composition import profile_service
from src.shared.dto import IdInputDTO
from src.static import ErrorEnum, SerializerErrors
from src.utils.exceptions import NotFoundException


from src.api.views.profile.profile.serializer import (
    UpsertProfileInputSerializer,
    ProfileOutputSerializer,
)


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    error_codes = SerializerErrors.CreateProfile.errors

    def get(self, *args, **kwargs):
        user_id = self.request.user.id
        profile = profile_service().get_profile(IdInputDTO(id=user_id))
        if profile is None:
            raise NotFoundException(
                error_type=[ErrorEnum.Profile.PROFILE_NOT_FOUND],
                message={"error": _("profile does not exist")},
            )
        return Response(
            data={
                "ok": True,
                "data": ProfileOutputSerializer(profile).data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, *args, **kwargs):
        dto = input_dto(
            UpsertProfileInputSerializer,
            self.request.data,
            UpsertProfileInputDTO,
            error_codes=self.error_codes,
            aliases={"photo": "photo_id"},
            profile_id=self.request.user.id,
        )
        result = profile_service().upsert_profile(dto)
        return Response(
            {
                "created": result.created,
                "data": ProfileOutputSerializer(result.profile).data,
                "status": status.HTTP_202_ACCEPTED,
            },
            status=status.HTTP_202_ACCEPTED,
        )
