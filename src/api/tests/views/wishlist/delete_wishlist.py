import uuid

from django.test import LiveServerTestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import RequestsClient

from src.apps.authentication.services import login_user_by_id
from src.utils.fakers import ProfileFactory, UserFactory, WishlistFactory


class DeleteWishlistAPITestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()
        self.faker = Faker()

        # Owner user + profile
        self.user_with_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)
        self.access_token_with_profile = login_user_by_id(
            self.user_with_profile.id
        ).get("access_token")

        # Wishlist owned by the profile
        self.wishlist = WishlistFactory(profile=self.profile)

        # Another user (not the owner)
        self.other_user = UserFactory()
        self.other_profile = ProfileFactory(profile_id=self.other_user.id)
        self.access_token_other = login_user_by_id(self.other_user.id).get(
            "access_token"
        )

    def make_request(self, wishlist_id, headers=None):
        """Helper to send DELETE requests."""
        url = self.live_server_url + reverse(
            "wishlist_action",
            kwargs={"id": wishlist_id},
        )
        return self.rc.delete(url, headers=headers)

    def test_unauthorized(self):
        """Deleting without an access token should return 401"""
        response = self.make_request(wishlist_id=self.wishlist.id)
        self.assertEqual(response.status_code, 401)

    def test_valid_delete_wishlist(self):
        """Owner should be able to delete their wishlist successfully"""
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            headers={"access": self.access_token_with_profile},
        )

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data.get("deleted"))
        self.assertEqual(json_data["status"], 200)

        # Verify wishlist is actually deleted
        from src.apps.wishlist.models import Wishlist

        exists = Wishlist.objects.filter(id=self.wishlist.id).exists()
        self.assertFalse(exists)

    def test_delete_wishlist_not_owner(self):
        """Another user (not the owner) should get 403 Forbidden"""
        response = self.make_request(
            wishlist_id=self.wishlist.id,
            headers={"access": self.access_token_other},
        )
        self.assertEqual(response.status_code, 403)

        # Wishlist should still exist
        from src.apps.wishlist.models import Wishlist

        self.assertTrue(Wishlist.objects.filter(id=self.wishlist.id).exists())

    def test_forbidden_wishlist_not_found(self):
        """Deleting a non-existing wishlist should raise NotFoundException"""
        non_existing_id = uuid.uuid4()

        response = self.make_request(
            wishlist_id=non_existing_id,
            headers={"access": self.access_token_with_profile},
        )

        self.assertEqual(response.status_code, 403)

        json_data = response.json()
        self.assertIn("error_type", json_data)
        self.assertIn("error", json_data.get("data", {}))
