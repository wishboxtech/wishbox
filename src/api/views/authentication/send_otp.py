import re

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.authentication.services import (
    create_one_time_password,
    one_time_password_exists,
)
from src.static import ErrorEnum
from src.utils.exceptions import BadRequestException


class SendOneTimePassword(APIView):
    permission_classes = []
    throttle_classes = []

    def post(self, *args, **kwargs):
        phone_number = self.request.data.get("phone_number")
        email = self.request.data.get("email")
        if not (phone_number or email):
            raise BadRequestException(
                message={"error": _("Phone number or Email must be submitted.")},
                error_type=[ErrorEnum.SendOneTimePassword.PHONE_NUMBER_IS_EMPTY],
            )

        if phone_number:
            phone_number_regex = r"^0\d{9,15}$"
            if not re.fullmatch(phone_number_regex, phone_number):
                raise BadRequestException(
                    message={"error": _("Phone number is not in valid format.")},
                    error_type=[ErrorEnum.SendOneTimePassword.INVALID_PHONE_NUMBER],
                )

        if one_time_password_exists(target=phone_number or email):
            raise BadRequestException(
                message={"message": _("OTP already sent.")},
                error_type=[ErrorEnum.SendOneTimePassword.OTP_ALREADY_SENT],
            )
        state = "phone_number" if phone_number else "email"
        otp_id = create_one_time_password(state, phone_number=phone_number, email=email)
        return Response(
            data={
                "ok": True,
                "data": {"otp_id": otp_id},
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
