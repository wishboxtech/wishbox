from contextlib import contextmanager, nullcontext
from dataclasses import replace
from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from src.apps.authentication.domain import User
from src.apps.authentication.domain.errors import (
    InvalidOTP,
    InvalidUserID,
    OTPAlreadySent,
)
from src.apps.authentication.dto import (
    CreateUserInputDTO,
    SendOTPInputDTO,
    TokensOutputDTO,
    VerifiedOTPOutputDTO,
    VerifyOTPInputDTO,
)
from src.apps.authentication.interfaces import (
    OTPRepository,
    TokenIssuer,
    UserRepository,
)
from src.apps.authentication.services import AuthenticationService
from src.shared.domain.errors import DomainValidationError
from src.shared.dto import IdInputDTO


class AuthenticationUnitTests(TestCase):
    def setUp(self):
        self.users = Mock(spec=UserRepository)
        self.otps = Mock(spec=OTPRepository)
        self.tokens = Mock(spec=TokenIssuer)
        self.notify = Mock()
        self.callbacks = []
        self.service = AuthenticationService(
            self.users,
            self.otps,
            self.tokens,
            self.notify,
            nullcontext,
            self.callbacks.append,
        )
        self.user = User(uuid4(), "09999999999", None, True, False, False)
        self.otps.exists.return_value = False
        self.otps.create.return_value = ("otp-id", "123456")
        self.tokens.issue.return_value = TokensOutputDTO(
            access_token="access", refresh_token="refresh"
        )

    def test_target_is_required_from_any_entrypoint(self):
        with self.assertRaises(DomainValidationError):
            self.service.send_otp(SendOTPInputDTO())
        self.otps.create.assert_not_called()

    def test_duplicate_otp_does_not_send_or_create(self):
        self.otps.exists.return_value = True
        with self.assertRaises(OTPAlreadySent):
            self.service.send_otp(SendOTPInputDTO(phone_number=self.user.phone_number))
        self.otps.create.assert_not_called()
        self.notify.assert_not_called()

    def test_sms_is_dispatched_only_by_after_commit(self):
        output = self.service.send_otp(
            SendOTPInputDTO(phone_number=self.user.phone_number, prefix="signup:")
        )
        self.assertEqual(output.otp_id, "otp-id")
        self.otps.create.assert_called_once_with(
            self.user.phone_number, "phone_number", "signup:"
        )
        self.notify.assert_not_called()
        self.callbacks[0]()
        self.notify.assert_called_once_with(self.user.phone_number, "123456")

    def test_email_does_not_send_sms(self):
        self.service.send_otp(SendOTPInputDTO(email="user@example.com"))
        self.assertEqual(self.callbacks, [])

    def test_verify_login_orchestrates_existing_user(self):
        self.otps.verify.return_value = VerifiedOTPOutputDTO(
            identifier=self.user.phone_number, state="phone_number"
        )
        self.users.find.return_value = self.user
        result = self.service.verify_and_login(
            VerifyOTPInputDTO(otp_id="id", otp_code="code")
        )
        self.assertEqual(result.access_token, "access")
        self.users.create.assert_not_called()
        self.users.record_login.assert_called_once_with(self.user.id)

    def test_guest_link_is_only_available_during_new_account_creation(self):
        self.service.guest_claims = Mock()
        self.service.guest_claims.claim.return_value = True
        self.otps.verify.return_value = VerifiedOTPOutputDTO(
            identifier=self.user.phone_number, state="phone_number"
        )
        self.users.find.return_value = None
        self.users.create.return_value = self.user
        dto = VerifyOTPInputDTO(otp_id="id", otp_code="code", guest_key="a" * 64)
        result = self.service.verify_and_login(dto)
        self.assertTrue(result.is_new_user)
        self.assertTrue(result.guest_claimed)
        self.service.guest_claims.claim.assert_called_once_with("a" * 64, self.user.id)
        self.users.find.return_value = self.user
        result = self.service.verify_and_login(dto)
        self.assertFalse(result.is_new_user)
        self.assertFalse(result.guest_claimed)
        self.assertEqual(self.service.guest_claims.claim.call_count, 1)

    def test_new_account_without_guest_consent_never_attempts_linking(self):
        self.service.guest_claims = Mock()
        self.otps.verify.return_value = VerifiedOTPOutputDTO(
            identifier=self.user.phone_number, state="phone_number"
        )
        self.users.find.return_value = None
        self.users.create.return_value = self.user
        result = self.service.verify_and_login(
            VerifyOTPInputDTO(otp_id="id", otp_code="code")
        )
        self.assertTrue(result.is_new_user)
        self.assertFalse(result.guest_claimed)
        self.service.guest_claims.claim.assert_not_called()

    def test_failed_otp_never_attempts_guest_linking(self):
        self.service.guest_claims = Mock()
        self.otps.verify.side_effect = InvalidOTP()
        with self.assertRaises(InvalidOTP):
            self.service.verify_and_login(
                VerifyOTPInputDTO(otp_id="id", otp_code="bad", guest_key="a" * 64)
            )
        self.service.guest_claims.claim.assert_not_called()
        self.users.create.assert_not_called()

    def test_verify_login_creates_user_before_issuing_tokens(self):
        events = []

        @contextmanager
        def transaction():
            events.append("enter")
            yield
            events.append("commit")

        self.service.transaction = transaction
        self.otps.verify.return_value = VerifiedOTPOutputDTO(
            identifier=self.user.phone_number, state="phone_number"
        )
        self.users.find.return_value = None
        self.users.create.return_value = self.user

        def issue(id):
            self.assertEqual(events, ["enter", "commit"])
            return TokensOutputDTO(access_token="a", refresh_token="r")

        self.tokens.issue.side_effect = issue
        self.service.verify_and_login(VerifyOTPInputDTO(otp_id="id", otp_code="code"))
        self.users.create.assert_called_once_with(
            CreateUserInputDTO(phone_number=self.user.phone_number)
        )

    def test_invalid_otp_never_creates_user_or_issues_tokens(self):
        self.otps.verify.side_effect = InvalidOTP()
        with self.assertRaises(InvalidOTP):
            self.service.verify_and_login(
                VerifyOTPInputDTO(otp_id="id", otp_code="wrong")
            )
        self.users.create.assert_not_called()
        self.tokens.issue.assert_not_called()
        self.users.record_login.assert_not_called()

    def test_inactive_user_cannot_login(self):
        self.users.get.return_value = replace(self.user, is_active=False)
        with self.assertRaises(InvalidUserID):
            self.service.login(IdInputDTO(id=self.user.id))
        self.tokens.issue.assert_not_called()
        self.users.record_login.assert_not_called()

    def test_failed_token_issue_does_not_count_as_a_login(self):
        self.users.get.return_value = self.user
        self.tokens.issue.side_effect = RuntimeError("Token storage unavailable")
        with self.assertRaises(RuntimeError):
            self.service.login(IdInputDTO(id=self.user.id))
        self.users.record_login.assert_not_called()
