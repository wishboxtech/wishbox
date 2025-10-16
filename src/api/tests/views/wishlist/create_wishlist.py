from django.test import LiveServerTestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import RequestsClient

from src.apps.authentication.services import login_user_by_id
from src.utils.fakers import ProfileFactory, UserFactory


class CreateWishlistTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()

        self.user_with_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)
        self.access_token_with_profile = login_user_by_id(
            self.user_with_profile.id
        ).get("access_token")

        self.solid_user = UserFactory()
        self.access_token = login_user_by_id(self.solid_user.id).get("access_token")

    def make_request(self, headers=None, data=None):
        url = self.live_server_url + reverse("wishlist")
        return self.rc.post(url, headers=headers, json=data)

    def test_unauthorized(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 401)

    def test_valid_create_wishlist(self):
        data = {
            "name": Faker().name(),
            "description": Faker().text(),
        }
        response = self.make_request(
            headers={"access": self.access_token_with_profile}, data=data
        )

        self.assertEqual(response.status_code, 201)
        data = response.json().get("data")
        self.assertEqual(data.get("name"), data["name"])
        self.assertEqual(data.get("description"), data["description"])
        self.assertEqual(response.json().get("created"), True)

    def test_invalid_create_wishlist(self):
        data = {
            "name": Faker().name(),
            "description": Faker().text(),
        }
        response = self.make_request(headers={"access": self.access_token}, data=data)

        self.assertEqual(response.status_code, 400)
        data = response.json().get("data")
