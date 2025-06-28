from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.authentication.services import (
    get_user_id_by_phone_number,
    verify_otp_and_get_user_phone, 
    login_user_by_id,
    create_user,
    user_registered
)

from settings import ACCESS_TTL
from src.static import ErrorEnum
from src.utils.exceptions import BadRequestException


class VerifyOneTimePasswordAPIView(APIView):
    
    def post(self, *args, **kwargs):
        otp_id = self.request.data.get("otp_id")
        otp_code = self.request.data.get("otp_code")
        error_messages = {}
        error_types = []
        if otp_id is None:
            error_messages["otp_id"] = _("otp_id must be submitted.")
            error_types.append(ErrorEnum.VerifyOneTimePassword.OTP_ID_IS_EMPTY)
        if otp_code is None:
            error_messages["otp_code"] = _("otp_code must be submitted.")
            error_types.append(
                ErrorEnum.VerifyOneTimePassword.OTP_CODE_IS_EMPTY
            )
        if len(error_types) != 0:
            raise BadRequestException(
                message=error_messages, error_type=error_types
            )
        phone_number = verify_otp_and_get_user_phone(otp_id, otp_code)
        if phone_number is None:
            raise BadRequestException(
                message={"error": _("otp is not valid.")},
                error_type=[ErrorEnum.VerifyOneTimePassword.INAVLID_OTP],
            )
        user_id = get_user_id_by_phone_number(phone_number=phone_number)
        if user_id is None:
            __, user_id, __ = create_user(phone_number=phone_number)
        data = login_user_by_id(user_id=user_id)
        return Response(
            data={
                "ok": True,
                "data": data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )