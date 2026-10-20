from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import RequestsClient

from src.core.composition import authentication_service
from src.shared.dto import IdInputDTO
from src.utils.fakers import AvatarFactory, ProfileFactory


class GetAvatarAPIViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()

        self.profile_with_avatar = ProfileFactory()
        self.avatar = AvatarFactory(profile=self.profile_with_avatar)
        self.access_token_with_profile = (
            authentication_service()
            .login(IdInputDTO(id=self.profile_with_avatar.profile_id))
            .model_dump()
            .get("access_token")
        )

    def make_request(self, headers=None):
        url = self.live_server_url + reverse("avatar")
        return self.rc.get(url, headers=headers)

    def test_unauthorized(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 401)

    def test_ok_response(self):
        response = self.make_request(headers={"access": self.access_token_with_profile})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("ok"), True)
        print(response.json())

    # should write more tests
    ...
