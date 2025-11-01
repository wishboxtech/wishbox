import uuid

from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import RequestsClient

from src.utils.fakers import (ProfileFactory, UserFactory, WishFactory,
                              WishlistFactory)


class GetWishesAPIViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()

        # create user, profile, and wishlist
        self.user = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user.id)
        self.wishlist = WishlistFactory(profile=self.profile)

        # add 3 wishes to the wishlist
        self.wishes = WishFactory.create_batch(3, wishlist=self.wishlist)

    def make_request(self, wishlist_id):
        url = self.live_server_url + reverse(
            "wishlist_action", kwargs={"id": wishlist_id}
        )
        return self.rc.get(url)

    def test_ok_response_with_wishes(self):
        """Should return all wishes of a wishlist"""
        response = self.make_request(wishlist_id=self.wishlist.id)
        self.assertEqual(response.status_code, 200)

        body = response.json()
        self.assertTrue(body.get("ok"))
        self.assertEqual(len(body.get("data")), 3)
        self.assertEqual(body.get("status"), 200)

    def test_ok_response_empty_wishlist(self):
        """Wishlist exists but has no wishes"""
        empty_wishlist = WishlistFactory(profile=self.profile)
        response = self.make_request(wishlist_id=empty_wishlist.id)
        self.assertEqual(response.status_code, 200)

        body = response.json()
        self.assertTrue(body.get("ok"))
        self.assertEqual(body.get("data"), [])
        self.assertEqual(body.get("status"), 200)

    def test_nonexistent_wishlist_id(self):
        """Wishlist does not exist → service should return [] or 404"""
        response = self.make_request(wishlist_id=uuid.uuid4())

        # depends on get_wishes_by_wishlist_id implementation
        # if it returns [], expect 200
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body.get("ok"))
        self.assertEqual(body.get("data"), [])
