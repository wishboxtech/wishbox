from django.test import TestCase

from src.apps.wishlist.services import (
    get_wishes_by_wishlist_id,
    get_wish_by_id,
)
from src.utils.fakers import ProfileFactory, WishlistFactory, WishFactory


class GetWishesServiceTestCase(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.other_profile = ProfileFactory()

        # Each profile gets one wishlist
        self.wishlist_for_profile = WishlistFactory(profile=self.profile)
        self.wishlist_for_other_profile = WishlistFactory(profile=self.other_profile)

        # Attach wishes to each wishlist
        self.wishes_for_profile = WishFactory.create_batch(
            3, wishlist=self.wishlist_for_profile
        )
        self.wishes_for_other_profile = WishFactory.create_batch(
            2, wishlist=self.wishlist_for_other_profile
        )

    def test_get_wishes_by_wishlist_id_returns_correct_data(self):
        # Wishes in profile’s wishlist
        wishes_data = get_wishes_by_wishlist_id(
            wishlist_id=self.wishlist_for_profile.id
        )
        self.assertEqual(len(wishes_data), 3)

        returned_ids = {w["id"] for w in wishes_data}
        expected_ids = {str(w.id) for w in self.wishes_for_profile}
        self.assertEqual(returned_ids, expected_ids)

        # Empty wishes for a new empty wishlist
        empty_wishlist = WishlistFactory(profile=self.profile)
        wishes_data = get_wishes_by_wishlist_id(wishlist_id=empty_wishlist.id)
        self.assertEqual(wishes_data, [])

    def test_get_wish_by_id_returns_correct_data(self):
        # Existing wish
        wish = self.wishes_for_profile[0]
        wish_data = get_wish_by_id(id=wish.id)
        self.assertEqual(wish_data["id"], str(wish.id))

        # Another profile’s wish
        wish = self.wishes_for_other_profile[0]
        wish_data = get_wish_by_id(id=wish.id)
        self.assertEqual(wish_data["id"], str(wish.id))

        # Non-existent wish
        wish_data = get_wish_by_id(id=99999)
        self.assertIsNone(wish_data)
