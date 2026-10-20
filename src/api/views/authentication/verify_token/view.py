from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.serialization import input_dto
from src.apps.authentication.dto import VerifyOTPInputDTO
from src.core.composition import authentication_service
from src.static import ErrorEnum


from src.api.views.authentication.verify_token.serializer import (
    VerifyOTPInputSerializer,
    VerifyOTPOutputSerializer,
)


class VerifyOneTimePasswordAPIView(APIView):
    permission_classes = []
    error_codes = {
        "otp_id": ErrorEnum.VerifyOneTimePassword.OTP_ID_IS_EMPTY,
        "otp_code": ErrorEnum.VerifyOneTimePassword.OTP_CODE_IS_EMPTY,
    }

    def post(self, *args, **kwargs):
        dto = input_dto(
            VerifyOTPInputSerializer,
            self.request.data,
            VerifyOTPInputDTO,
            error_codes=self.error_codes,
        )
        result = authentication_service().verify_and_login(dto)
        return Response(
            {
                "ok": True,
                "data": VerifyOTPOutputSerializer(result).data,
                "status": status.HTTP_200_OK,
            }
        )
