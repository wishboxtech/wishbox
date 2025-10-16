from datetime import timedelta

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from settings import ACCESS_TTL
from src.apps.authentication.services import refresh
from src.static import ErrorEnum
from src.utils.exceptions import BadRequestException


class RefreshTokenAPIView(APIView):
    permission_classes = []

    def post(self, *args, **kwargs):
        refresh_token = self.request.data.get("refresh_token")
        if refresh_token is None:
            raise BadRequestException(
                message={"error": _("refresh_token must be submitted.")},
                error_type=[ErrorEnum.RefreshToken.REFRESH_IS_EMPTY],
            )
        access_token, refresh_token = refresh(token=refresh_token)
        response = Response(
            data={
                "ok": True,
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
        expires = timezone.now() + timedelta(seconds=ACCESS_TTL)
        response.set_cookie(
            key="HTTP_ACCESS",
            value=access_token,
            expires=expires,
            httponly=True,
            secure=True,
            samesite="None",
        )
        return response
