import uuid

from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import RequestsClient

from src.utils.fakers import (ProfileFactory, UserFactory, WishFactory,
                              WishlistFactory)


class GetWishByIdAPIViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()

        # create user, profile, wishlist, and one wish
        self.user = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user.id)
        self.wishlist = WishlistFactory(profile=self.profile)
        self.wish = WishFactory(wishlist=self.wishlist)

    def make_request(self, wish_id):
        url = self.live_server_url + reverse("wish_by_id", kwargs={"id": wish_id})
        return self.rc.get(url)

    def test_ok_response_with_existing_wish(self):
        """Should return 200 OK with the correct wish data."""
        response = self.make_request(wish_id=self.wish.id)
        self.assertEqual(response.status_code, 200)

        body = response.json()
        self.assertTrue(body.get("ok"))
        self.assertEqual(body.get("status"), 200)

        data = body.get("data")
        self.assertIsInstance(data, dict)
        self.assertEqual(str(self.wish.id), data.get("id"))
        self.assertEqual(self.wish.name, data.get("name"))
        self.assertEqual(self.wish.description, data.get("description"))
        self.assertEqual(self.wish.price, int(data.get("price")))

    def test_nonexistent_wish_returns_404(self):
        """Should raise NotFoundException and return 404 for non-existent wish ID."""
        non_existent_id = uuid.uuid4()
        response = self.make_request(wish_id=non_existent_id)
        self.assertEqual(response.status_code, 404)

        body = response.json()
        self.assertFalse(body.get("ok"))
        self.assertEqual(body.get("status"), 404)
