from unittest.mock import patch

from django.test import TestCase

from src.apps.authentication.services import (
    create_one_time_password,
    verify_otp_and_get_user_phone,
)
from src.utils.fakers import UserFactory


class VerifyOTPServiceTestCase(TestCase):
    @patch("src.apps.authentication.services.create_otp.send_sms_otp")
    def setUp(self, *_):
        self.user = UserFactory()
        self.otp_code = "265472"
        with patch(
            "src.apps.authentication.models.otp.generate_otp",
            new=lambda *args: self.otp_code,
        ):
            self.otp_id = create_one_time_password(self.user.phone_number)

    def test_valid_verify_otp_and_get_user_phone_service(self):
        user_phone = verify_otp_and_get_user_phone(
            otp_id=self.otp_id, otp_code=self.otp_code
        )
        self.assertEqual(user_phone, str(self.user.phone_number))

    def test_invalid_verify_otp_and_get_user_phone_service(self):
        user_phone = verify_otp_and_get_user_phone(
            otp_id="invalid", otp_code=self.otp_code
        )
        self.assertIsNone(user_phone)
        user_phone = verify_otp_and_get_user_phone(
            otp_id=self.otp_id, otp_code="invalid"
        )
        self.assertIsNone(user_phone)
        with patch("django.core.cache.cache.ttl", new=lambda x: 0):
            user_phone = verify_otp_and_get_user_phone(
                otp_id=self.otp_id, otp_code=self.otp_code
            )
            self.assertIsNone(user_phone)
