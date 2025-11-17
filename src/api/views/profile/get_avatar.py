from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.profile.services import get_user_avatar
from src.static import ErrorEnum
from src.utils.exceptions import NotFoundException


class GetAvatarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        profile_id = self.request.user.id
        avatar = get_user_avatar(profile_id=profile_id)
        if avatar is None:
            raise NotFoundException(
                error_type=[ErrorEnum.Profile.AVATAR_NOT_FOUND],
                message={"error": _("avatar does not exist")},
            )

        return Response(
            data={
                "ok": True,
                "data": avatar,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
