from django.test import TestCase

from src.apps.wishlist.services import get_wishlist_by_id, get_wishlists_by_profile
from src.utils.fakers import ProfileFactory, WishlistFactory


class GetWishlistsServiceTestCase(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.other_profile = ProfileFactory()

        self.wishlists_for_profile = WishlistFactory.create_batch(
            3, profile=self.profile
        )

        self.wishlists_for_other_profile = WishlistFactory.create_batch(
            2, profile=self.other_profile
        )

    def test_get_wishlists_by_profile_returns_correct_data(self):

        wishlists_data = get_wishlists_by_profile(profile_id=self.profile.profile_id)
        self.assertEqual(len(wishlists_data), 3)
        returned_ids = {w["id"] for w in wishlists_data}
        expected_ids = {str(w.id) for w in self.wishlists_for_profile}
        self.assertEqual(returned_ids, expected_ids)

        new_profile = ProfileFactory()
        wishlists_data = get_wishlists_by_profile(profile_id=new_profile.profile_id)
        self.assertEqual(wishlists_data, [])

    def test_get_wishlist_by_id_returns_correct_data(self):

        wishlist = self.wishlists_for_profile[0]
        wishlist_data = get_wishlist_by_id(id=wishlist.id)
        self.assertEqual(wishlist_data["id"], str(wishlist.id))

        wishlist = self.wishlists_for_other_profile[0]
        wishlist_data = get_wishlist_by_id(id=wishlist.id)
        self.assertEqual(wishlist_data["id"], str(wishlist.id))

        wishlist_data = get_wishlist_by_id(id=99999)
        self.assertIsNone(wishlist_data)
