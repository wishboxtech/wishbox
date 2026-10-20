from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from settings import ACCESS_TTL
from src.api.serialization import input_dto
from src.apps.authentication.dto import RefreshInputDTO
from src.core.composition import authentication_service
from src.static import ErrorEnum


from src.api.views.authentication.refresh_token.serializer import (
    RefreshTokenInputSerializer,
    RefreshTokenOutputSerializer,
)


class RefreshTokenAPIView(APIView):
    permission_classes = []

    def post(self, *args, **kwargs):
        dto = input_dto(
            RefreshTokenInputSerializer,
            self.request.data,
            RefreshInputDTO,
            aliases={"refresh_token": "token"},
            error_codes={"refresh_token": ErrorEnum.RefreshToken.REFRESH_IS_EMPTY},
        )
        result = authentication_service().refresh(dto)
        access_token = result.access_token
        response = Response(
            data={
                "ok": True,
                "data": RefreshTokenOutputSerializer(result).data,
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
