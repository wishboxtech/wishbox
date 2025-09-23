from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import RequestsClient
from faker import Faker

from src.apps.authentication.services import login_user_by_id
from src.utils.fakers import UserFactory, ProfileFactory, WishlistFactory


class CreateWishTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()
        faker = Faker()

        # user WITH profile & wishlist (valid case)
        self.user_with_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)
        self.wishlist = WishlistFactory(profile=self.profile)

        self.access_token_with_profile = login_user_by_id(
            self.user_with_profile.id
        ).get("access_token")

        # user WITHOUT profile (invalid case, should fail permission check)
        self.solid_user = UserFactory()
        self.access_token = login_user_by_id(self.solid_user.id).get("access_token")

        # default payload for creating a wish
        self.valid_payload = {
            "name": faker.word(),
            "description": faker.text(),
            "price": faker.random_number(digits=3),
            "cover": None,  # skipping file upload for now
        }

    def make_request(self, wishlist_id, headers=None, data=None):
        url = self.live_server_url + reverse("wish", kwargs={"id": wishlist_id})
        return self.rc.post(url, headers=headers, json=data)

    def test_unauthorized(self):
        """No token should return 401"""
        response = self.make_request(wishlist_id=self.wishlist.id)
        self.assertEqual(response.status_code, 401)

    def test_valid_create_wish(self):
        """Owner of wishlist can add a wish"""
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            headers={"access": self.access_token_with_profile},
            data=self.valid_payload,
        )

        self.assertEqual(response.status_code, 201)
        res_data = response.json().get("data")
        self.assertEqual(res_data.get("name"), self.valid_payload["name"])
        self.assertEqual(res_data.get("description"), self.valid_payload["description"])
        self.assertEqual(res_data.get("price"), str(self.valid_payload["price"]))
        self.assertEqual(response.json().get("created"), True)

    def test_invalid_create_wish_not_owner(self):
        """Non-owner should fail object permission check"""
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            headers={"access": self.access_token},
            data=self.valid_payload,
        )
        self.assertEqual(response.status_code, 403)

    def test_invalid_create_wish_bad_data(self):
        """Missing required fields should raise BadRequestException"""
        bad_payload = {
            "name": "",  # invalid
            "description": "Some text",
        }
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            headers={"access": self.access_token_with_profile},
            data=bad_payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json().get("error_type"), ["CREATE_WISH_SERIALZER_INVALID_NAME"]
        )
