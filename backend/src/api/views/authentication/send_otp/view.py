from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serialization import input_dto
from src.apps.authentication.dto import SendOTPInputDTO
from src.core.composition import authentication_service
from src.static import ErrorEnum


from src.api.views.authentication.send_otp.serializer import (
    SendOTPInputSerializer,
    SendOTPOutputSerializer,
)


class SendOneTimePassword(APIView):
    permission_classes = []
    throttle_classes = []
    error_codes = {
        "phone_number": ErrorEnum.SendOneTimePassword.INVALID_PHONE_NUMBER,
        "email": ErrorEnum.SendOneTimePassword.PHONE_NUMBER_IS_EMPTY,
    }

    def post(self, *args, **kwargs):
        dto = input_dto(
            SendOTPInputSerializer,
            self.request.data,
            SendOTPInputDTO,
            error_codes=self.error_codes,
        )
        result = authentication_service().send_otp(dto)
        return Response(
            {
                "ok": True,
                "data": SendOTPOutputSerializer(result).data,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
