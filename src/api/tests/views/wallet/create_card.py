from django.test import LiveServerTestCase
from rest_framework.test import RequestsClient
from django.urls import reverse
from src.apps.authentication.services import login_user_by_id
from src.static.error_enum import ErrorEnum
from src.static.serializer_errors import SerializerErrors
from src.utils.fakers import UserFactory


class CreateCardAPIViewTestCase(LiveServerTestCase):

    def setUp(self, *_):
        self.rc = RequestsClient()
        self.user = UserFactory()
        self.access_token = login_user_by_id(self.user.id).get("access_token")

    def make_request(self, headers=None, data=None):
        url = self.live_server_url + reverse(
            "card",
        )
        return self.rc.post(url, headers=headers, json=data)

    def test_unauthorized(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 401)

    def test_ok_response(self):
        response = self.make_request(
            headers={"access": self.access_token},
            data={"card_number": "1111222233334444"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get("ok"), True)
        self.assertEqual(response.json().get("status"), 201)

    def test_bad_request(self):
        response = self.make_request(
            headers={"access": self.access_token},
            data={"card_number": "invalid"},
        )
        self.assertEqual(response.status_code, 400)
