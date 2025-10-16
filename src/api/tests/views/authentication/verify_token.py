from unittest.mock import AsyncMock, patch

from django.test import LiveServerTestCase
from factory.faker import faker
from rest_framework.test import RequestsClient

from src.apps.authentication.services import create_one_time_password
from src.static import ErrorEnum
from src.utils.fakers import UserFactory


class VerifyOneTimePasswordViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()
        self.user = UserFactory()

    def make_request(self, data=None):
        return self.rc.post("http://testserver/api/V0.0.0/auth/otp/verify/", json=data)

    def test_bad_request_response(self):
        def post_bad_request(error_type, data=None):
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, 400)
            error_set = set(error_type)
            data_error = response.json().get("error_type")
            data_error_set = set(data_error)
            self.assertSetEqual(
                error_set,
                data_error_set,
            )

        post_bad_request(
            error_type=[
                ErrorEnum.VerifyOneTimePassword.OTP_ID_IS_EMPTY,
                ErrorEnum.VerifyOneTimePassword.OTP_CODE_IS_EMPTY,
            ],
        )

        post_bad_request(
            error_type=[ErrorEnum.VerifyOneTimePassword.INAVLID_OTP],
            data={"otp_id": "some id", "otp_code": "some code"},
        )

    @patch("src.utils.nats.publish.NCSC.connect", side_effect=AsyncMock())
    @patch("src.utils.nats.publish.publish", side_effect=AsyncMock())
    @patch("src.utils.nats.publish.NCSC.disconnect", side_effect=AsyncMock())
    def test_ok_response(self, *_):
        def post_ok(data):
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, 200)
            data = response.json().get("data")
            self.assertIn("access_token", data.keys())
            self.assertIn("refresh_token", data.keys())

        otp_code = "123423"
        with patch(
            "src.apps.authentication.models.otp.generate_otp",
            new=lambda *args: otp_code,
        ):
            otp_id = create_one_time_password(phone_number=self.user.phone_number)
            post_ok(
                data={"otp_id": otp_id, "otp_code": otp_code},
            )
        phone_number = faker.Faker().numerify("09#########")
        with patch(
            "src.apps.authentication.models.otp.generate_otp",
            new=lambda *args: otp_code,
        ):
            otp_id = create_one_time_password(phone_number=phone_number)
            post_ok(
                data={"otp_id": otp_id, "otp_code": otp_code},
            )
            self.assertIsNotNone(phone_number)
