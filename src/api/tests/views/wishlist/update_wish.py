import uuid

from django.test import LiveServerTestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import RequestsClient

from src.apps.authentication.services import login_user_by_id
from src.utils.fakers import ProfileFactory, UserFactory, WishFactory, WishlistFactory


class UpdateWishAPITestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()
        self.faker = Faker()

        # Owner user + profile
        self.user_with_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)
        self.access_token_with_profile = login_user_by_id(
            self.user_with_profile.id
        ).get("access_token")

        # Wishlist + Wish
        self.wishlist = WishlistFactory(profile=self.profile)
        self.wish = WishFactory(
            wishlist=self.wishlist,
            name="Old Phone",
            description="Broken but working",
            price=500,
        )

        # Another user (not owner)
        self.other_user = UserFactory()
        self.other_profile = ProfileFactory(profile_id=self.other_user.id)
        self.access_token_other = login_user_by_id(self.other_user.id).get(
            "access_token"
        )

    def make_request(self, wishlist_id, wish_id, headers=None, data=None):
        url = self.live_server_url + reverse(
            "wish_action",
            args=[wishlist_id, wish_id],
        )
        return self.rc.patch(url, headers=headers, json=data)

    def test_unauthorized(self):
        """No token should return 401"""
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            wish_id=self.wish.id,
        )
        self.assertEqual(response.status_code, 401)

    def test_valid_update_wish(self):
        """Owner should be able to update successfully"""
        new_name = self.faker.word()
        new_description = self.faker.text()
        new_price = 1200
        data = {
            "name": new_name,
            "description": new_description,
            "price": new_price,
        }

        response = self.make_request(
            wishlist_id=self.wishlist.id,
            wish_id=self.wish.id,
            headers={"access": self.access_token_with_profile},
            data=data,
        )

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data.get("updated"))
        self.assertEqual(json_data["data"]["name"], new_name)
        self.assertEqual(json_data["data"]["description"], new_description)
        self.assertEqual(json_data["data"]["price"], str(new_price))

    def test_update_wish_not_owner(self):
        """Another user should not be able to update"""
        data = {
            "name": self.faker.word(),
            "description": self.faker.text(),
            "price": 999,
        }
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            wish_id=self.wish.id,
            headers={"access": self.access_token_other},
            data=data,
        )
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_update_wish_invalid_id(self):
        """Updating non-existing wish should return 400 BadRequestException"""
        data = {
            "name": self.faker.word(),
            "description": self.faker.text(),
            "price": 1000,
        }
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            wish_id=uuid.uuid4(),
            headers={"access": self.access_token_with_profile},
            data=data,
        )
        self.assertEqual(response.status_code, 400)

    def test_update_wish_invalid_validation_error(self):
        """Sending invalid data should return 400 with error_type"""
        data = {
            "name": self.faker.word(),
            "description": None,  # invalid because required
        }
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            wish_id=self.wish.id,
            headers={"access": self.access_token_with_profile},
            data=data,
        )
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertIn("error_type", json_data)
