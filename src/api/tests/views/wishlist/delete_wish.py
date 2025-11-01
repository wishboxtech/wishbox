import uuid

from django.test import LiveServerTestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import RequestsClient

from src.apps.authentication.services import login_user_by_id
from src.utils.fakers import (ProfileFactory, UserFactory, WishFactory,
                              WishlistFactory)


class DeleteWishAPITestCase(LiveServerTestCase):
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

    def make_request(self, wishlist_id, wish_id, headers=None):
        """Helper to perform DELETE request"""
        url = self.live_server_url + reverse(
            "wish_action",
            args=[wishlist_id, wish_id],
        )
        return self.rc.delete(url, headers=headers)

    def test_unauthorized(self):
        """Deleting without token should return 401 Unauthorized"""
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            wish_id=self.wish.id,
        )
        self.assertEqual(response.status_code, 401)

    def test_valid_delete_wish(self):
        """Owner should be able to delete a wish successfully"""
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            wish_id=self.wish.id,
            headers={"access": self.access_token_with_profile},
        )

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data.get("deleted"))
        self.assertEqual(json_data["status"], 200)

        # Verify wish is actually deleted
        from src.apps.wishlist.models import Wish

        exists = Wish.objects.filter(id=self.wish.id).exists()
        self.assertFalse(exists)

    def test_delete_wish_not_owner(self):
        """Another user should not be able to delete someone else's wish"""
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            wish_id=self.wish.id,
            headers={"access": self.access_token_other},
        )
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Wish should still exist
        from src.apps.wishlist.models import Wish

        self.assertTrue(Wish.objects.filter(id=self.wish.id).exists())

    def test_delete_wish_not_found(self):
        """Deleting a non-existing wish should raise NotFoundException (400 or 404)"""
        non_existing_id = uuid.uuid4()

        response = self.make_request(
            wishlist_id=self.wishlist.id,
            wish_id=non_existing_id,
            headers={"access": self.access_token_with_profile},
        )

        self.assertEqual(response.status_code, 404)
        json_data = response.json()
        self.assertIn("error_type", json_data)
        self.assertIn("error", json_data.get("data", {}))
