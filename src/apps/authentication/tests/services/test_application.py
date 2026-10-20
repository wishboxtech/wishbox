from unittest.mock import Mock, patch

from django.core.cache import cache
from django.test import TestCase

from src.apps.authentication.domain.errors import InvalidOTP, OTPAlreadySent
from src.apps.authentication.dto import (
    CreateUserInputDTO,
    SendOTPInputDTO,
    VerifyOTPInputDTO,
)
from src.apps.authentication.functions import validate_token
from src.core.composition import authentication_service
from src.shared.dto import IdInputDTO


class AuthenticationServiceIntegrationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.service = authentication_service()

    def test_create_get_and_login_user(self):
        user = self.service.create_user(
            CreateUserInputDTO(phone_number="09999999999", password="foo")
        )
        self.assertEqual(self.service.get_user(IdInputDTO(id=user.id)), user)
        tokens = self.service.login(IdInputDTO(id=user.id))
        self.assertTrue(validate_token(tokens.access_token))

    def test_prefixed_otp_and_verification(self):
        with patch(
            "src.apps.authentication.repositories.otp.generate_otp",
            return_value="123456",
        ):
            output = self.service.send_otp(
                SendOTPInputDTO(phone_number="09999999999", prefix="signup:")
            )
        verified = self.service.verify_otp(
            VerifyOTPInputDTO(otp_id=output.otp_id, otp_code="123456", prefix="signup:")
        )
        self.assertEqual(verified.identifier, "09999999999")
        with self.assertRaises(InvalidOTP):
            self.service.verify_otp(
                VerifyOTPInputDTO(otp_id=output.otp_id, otp_code="123456")
            )
        with self.assertRaises(InvalidOTP):
            self.service.verify_otp(
                VerifyOTPInputDTO(
                    otp_id=output.otp_id, otp_code="wrong", prefix="signup:"
                )
            )

    def test_duplicate_otp_is_rejected(self):
        self.service.send_otp(SendOTPInputDTO(phone_number="09999999999"))
        with self.assertRaises(OTPAlreadySent):
            self.service.send_otp(SendOTPInputDTO(phone_number="09999999999"))

    def test_notify_is_registered_after_commit(self):
        self.service.notify = Mock()
        with self.captureOnCommitCallbacks(execute=True):
            self.service.send_otp(SendOTPInputDTO(phone_number="09999999999"))
            self.service.notify.assert_not_called()
        self.service.notify.assert_called_once()

    def test_verify_and_login_orchestrates_new_user(self):
        with patch(
            "src.apps.authentication.repositories.otp.generate_otp",
            return_value="123456",
        ):
            output = self.service.send_otp(SendOTPInputDTO(phone_number="09999999999"))
        tokens = self.service.verify_and_login(
            VerifyOTPInputDTO(otp_id=output.otp_id, otp_code="123456")
        )
        self.assertTrue(validate_token(tokens.access_token))
