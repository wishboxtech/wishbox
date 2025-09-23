from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from src.apps.profile.services import get_profile_by_user_id

from src.static import ErrorEnum
from src.utils.exceptions import NotFoundException


class GetProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user_id = self.request.user.id
        profile = get_profile_by_user_id(id=user_id)
        if profile is None:
            raise NotFoundException(
                error_type=[ErrorEnum.Profile.PROFILE_NOT_FOUND],
                message={"error": _("profile does not exist")},
            )
        return Response(
            data={
                "ok": True,
                "data": profile,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
