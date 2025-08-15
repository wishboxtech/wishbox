from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import RequestsClient
from faker import Faker
import uuid
from src.apps.authentication.services import login_user_by_id
from src.utils.fakers import UserFactory, ProfileFactory, WishlistFactory


class UpdateWishlistTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()

        self.user_with_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)
        self.access_token_with_profile = login_user_by_id(
            self.user_with_profile.id
        ).get("access_token")

        self.wishlist = WishlistFactory(profile=self.profile)
        self.solid_user = UserFactory()
        self.access_token = login_user_by_id(self.solid_user.id).get("access_token")

    def make_request(self, id, headers=None, data=None):
        url = self.live_server_url + reverse("wishlist_with_id", args=[id])
        return self.rc.patch(url, headers=headers, json=data)

    def test_unauthorized(self):
        response = self.make_request(id=None)
        self.assertEqual(response.status_code, 401)

    def test_valid_update_wishlist(self):
        new_name = Faker().name()
        data = {
            "name": new_name,
            "description": Faker().text(),
        }
        response = self.make_request(
            headers={"access": self.access_token_with_profile},
            data=data,
            id=self.wishlist.id,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json().get("data")
        self.assertEqual(data.get("name"), data["name"])
        self.assertEqual(data.get("description"), data["description"])
        self.assertEqual(response.json().get("updated"), True)

    def test_invalid_create_wishlist(self):
        data = {
            "name": Faker().name(),
            "description": Faker().text(),
        }
        response = self.make_request(
            headers={"access": self.access_token},
            data=data,
            id=uuid.uuid4(),
        )

        self.assertEqual(response.status_code, 400)
