from datetime import timedelta

from django.test import LiveServerTestCase
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import RequestsClient

from settings import REFRESH_TTL
from src.apps.authentication.services import login_user_by_id
from src.static import ErrorEnum
from src.utils.fakers import UserFactory


class RefreshTokenAPIViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()
        self.user = UserFactory()
        self.refresh_token_for_valid = login_user_by_id(self.user.id).get(
            "refresh_token"
        )
        self.refresh_token_for_invalid = login_user_by_id(self.user.id).get(
            "refresh_token"
        )

    def make_request(self, data=None):
        return self.rc.post(
            "http://testserver/api/V0.0.0/auth/otp/refresh/", json=data
        )

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
            error_type=[ErrorEnum.RefreshToken.REFRESH_IS_EMPTY],
        )
        with freeze_time(
            timezone.now() + timedelta(minutes=REFRESH_TTL * 60, seconds=1)
        ):
            post_bad_request(
                data={"refresh_token": self.refresh_token_for_invalid},
                error_type=[ErrorEnum.RefreshToken.TOKEN_IS_NOT_VALID],
            )

    def test_ok_response(self):
        def post_ok(data):
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, 200)
            data = response.json().get("data")
            access = data.get("access_token")
            refresh = data.get("refresh_token")
            self.assertIsNotNone(access)
            self.assertIsNotNone(refresh)
            self.assertIsInstance(access, str)
            self.assertIsInstance(refresh, str)

        post_ok(data={"refresh_token": self.refresh_token_for_valid})
