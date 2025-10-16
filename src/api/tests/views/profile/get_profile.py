from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import RequestsClient

from src.apps.authentication.services import login_user_by_id
from src.utils.fakers import ProfileFactory, UserFactory


class GetProfileAPIViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()

        self.user_with_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)
        self.access_token_with_profile = login_user_by_id(self.user_with_profile.id).get("access_token")

        self.solid_user = UserFactory()
        self.access_token = login_user_by_id(self.solid_user.id).get("access_token")

    def make_request(self, headers=None):
        url = self.live_server_url + reverse("profile")
        return self.rc.get(url, headers=headers)
    
    def test_unauthorized(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 401)
    
    def test_ok_response(self):
        response = self.make_request(
            headers={"access": self.access_token_with_profile}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("ok"), True)
        data = response.json().get("data")
        self.assertEqual(data.get("profile_id"), str(self.user_with_profile.id))
    
    def test_profile_not_found(self):
        response = self.make_request(
            headers={"access": self.access_token}
        )
        self.assertEqual(response.status_code, 404)