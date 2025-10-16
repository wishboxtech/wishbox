from unittest.mock import patch

from django.test import LiveServerTestCase
from rest_framework.test import RequestsClient

from src.static import ErrorEnum, SerializerErrors
from src.utils.fakers import UserFactory


class SendOneTimePasswordAPIViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()
        self.user = UserFactory()
        self.user_for_already_sent = UserFactory()

    def make_request(self, data=None):
        return self.rc.post("http://testserver/api/V0.0.0/auth/otp/", json=data)

    @patch("nats.aio.client.Client.connect")
    @patch("nats.js.client.JetStreamContext.publish")
    @patch("nats.aio.client.Client.close")
    def test_bad_request_response(self, *_):
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
            error_type=[ErrorEnum.SendOneTimePassword.PHONE_NUMBER_IS_EMPTY]
        )

        self.make_request(
            data={"phone_number": self.user_for_already_sent.phone_number}
        )

        post_bad_request(
            error_type=[ErrorEnum.SendOneTimePassword.OTP_ALREADY_SENT],
            data={"phone_number": self.user_for_already_sent.phone_number},
        )

    @patch("nats.aio.client.Client.connect")
    @patch("nats.js.client.JetStreamContext.publish")
    @patch("nats.aio.client.Client.close")
    def test_created_response(self, *_):
        def created_response(data=None):
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, 201)

        created_response(data={"phone_number": self.user.phone_number})

        with patch.multiple(
            "django.core.cache.cache",
            ttl=lambda x: 0,
            set=lambda key, value, timeout=None, nx=False: True,
        ):
            created_response(data={"phone_number": self.user.phone_number})

        with patch.multiple(
            "django.core.cache.cache",
            ttl=lambda x: 0,
            set=lambda key, value, timeout=None, nx=False: True,
        ):
            created_response(data={"phone_number": self.user.phone_number})

        with patch.multiple(
            "django.core.cache.cache",
            ttl=lambda x: 0,
            set=lambda key, value, timeout=None, nx=False: True,
        ):
            created_response(data={"phone_number": "09999999999"})
